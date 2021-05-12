function isElementVisible(page, cssSelector){
    let visible = true;
    page
      .waitForSelector(cssSelector, { visible: true, timeout: 2000 })
      .catch(() => {
        visible = false;
      });
    return visible;
  };

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

const scraperObject = {
    url: 'https://japanfigure.vn/collections/all',
    async scraper(browser){
        let page = await browser.newPage();
        console.log(`Navigating to ${this.url}...`);
        await page.goto(this.url);
        
        const selectorForLoadMoreButton = '.btn-loading'
        let loadMoreVisible = await isElementVisible(page, selectorForLoadMoreButton);
        // while (loadMoreVisible) {
        //     await page
        //         .click(selectorForLoadMoreButton)
        //         .catch(() => {});
        //     loadMoreVisible = await isElementVisible(page, selectorForLoadMoreButton);
        // }
        // check button
        // const button_load = await page.evaluate(() => {
            
        // })
        
        

        // Get the link to all the required books
        await page.evaluate(()=>{
            
            i=0;
            var inter = setInterval(() => {
                document.getElementsByClassName("btn-loading")[0].click();
                i++; 
                if (i == 2000){
                    clearInterval(inter);
                }
            }, 100);
        })

        await page.waitForTimeout(1200000)

        const a = await page.evaluate(()=>{
            const item = document.getElementsByClassName("product-title");
                let arr = [];
                console.log("total item: " + item.length);
                for (let i=0; i<item.length; i++) {
                    const item_s = $(".product-title a")[i]
                    arr.push({
                        item_name: item_s.title,
                        item_url: item_s.href
                    })
                }
            return arr
        })
        console.log(a,a.length)

        var fs = require('fs');

        fs.writeFileSync('item_link.json', JSON.stringify(a), function(err) {
            if (err) throw err;
            console.log('saved!')
        })
        
    }
}


module.exports = scraperObject;

