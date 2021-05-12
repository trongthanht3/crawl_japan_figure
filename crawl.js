await page.setExtraHTTPHeaders({
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
});

await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36');

await page.setViewport({width: 800, height: 1080});

let page = await browser.newPage();
await page.goto('https://japanfigure.vn/collections/all');

page.waitFor(3000);





await browser.close();