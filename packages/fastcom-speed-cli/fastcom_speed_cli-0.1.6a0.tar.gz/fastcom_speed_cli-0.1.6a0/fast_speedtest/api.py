import asyncio
import json
import sys

from typing import NamedTuple

from playwright.async_api import StorageState
from playwright.async_api import async_playwright


class fast_config_t(NamedTuple):
    minDuration: int = 5
    maxDuration: int = 30
    measureUploadLatency: bool = False
    minConnections: int = 1
    maxConnections: int = 8
    shouldPersist: bool = True
    showAdvanced: bool = True
    # __test__: int = 1


def gen_local_storage(
    config: fast_config_t
):

    local_storage_data = config._asdict()

    return StorageState(
        cookies=[],
        origins=[
            {
                'origin': 'https://fast.com',
                'localStorage': [
                    {
                        'name': key,
                        'value': json.dumps(value)
                    } for key, value in local_storage_data.items()
                ]
            }
        ]
    )


class speedtest_config_t(NamedTuple):
    fast_config: fast_config_t = fast_config_t()
    upload: bool = False
    check_interval: float = 1.0
    print: bool = True
    browser_name: str = "chromium"


DEFAULT_SPEEDTEST_CONF = speedtest_config_t()


async def run_speedtest(config: speedtest_config_t = DEFAULT_SPEEDTEST_CONF):
    results = []
    async with async_playwright() as p:
        browser = await getattr(p, config.browser_name).launch(headless=True)
        context = await browser.new_context(storage_state=gen_local_storage(config.fast_config))
        page = await context.new_page()
        await page.goto("https://fast.com")
        while True:
            await asyncio.sleep(config.check_interval)
            error = None
            error_elem = page.locator('#error-results-msg')
            if await error_elem.is_visible():
                error_text = await error_elem.text_content()
                error = error_text.strip() if error_text else None
                print(error, file=sys.stderr)
                results.append({"error": error})
                break
            # error: ($('#error-results-msg')?.textContent || '').trim(),
            result = await page.evaluate(
                '''(function(){
    const $ = document.querySelector.bind(document);

    return {
        downloadSpeed: Number($('#speed-value')?.textContent) || 0,
        uploadSpeed: Number($('#upload-value')?.textContent) || 0,
        downloadUnit: ($('#speed-units')?.textContent || '').trim(),
        downloaded: Number($('#down-mb-value')?.textContent?.trim()) || 0,
        uploadUnit: ($('#upload-units')?.textContent || '').trim(),
        uploaded: Number($('#up-mb-value')?.textContent?.trim()) || 0,
        latency: Number($('#latency-value')?.textContent?.trim()) || 0,
        bufferBloat: Number($('#bufferbloat-value')?.textContent?.trim()) || 0,
        userLocation: ($('#user-location')?.textContent || '').trim(),
        userIp: ($('#user-ip')?.textContent || '').trim(),
        serverLocation: ($('#server-locations')?.textContent || '').trim().split('\xa0\xa0|\xa0\xa0'),
        isDone: Boolean($('#speed-value.succeeded') && $('#upload-value.succeeded'))
    };
})();
'''
                )
            if config.print:
                print('Speed Test Results:', result, file=sys.stderr)
            results.append(result)
            if not config.upload and result["uploadSpeed"]:
                break
            if result["isDone"]:
                break
            
        await context.close()
        await browser.close()    
    return results
