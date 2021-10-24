const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());
const chromePaths = require('chrome-paths');
const readlineSync = require('readline-sync');
const url = readlineSync.question('Masukan URL Stream nya: ');
const view = readlineSync.question('Masukan jumlah view (ex. 10) : ')
;(async () => {
    for (let index = 0; index < view; index++) {
        const args = [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-infobars',
            '--ignore-certifcate-errors',
            '--ignore-certifcate-errors-spki-list',
            '--disable-accelerated-2d-canvas',
            '--no-zygote',
            '--no-first-run',
            '--disable-dev-shm-usage',
            '--window-size=300x200',
            '--proxy-server=http://isp2.hydraproxy.com:9989' //change your proxy server
        ];

        const browser = await puppeteer.launch({
            headless: false,
            executablePath: chromePaths.chrome,
            ignoreHTTPSErrors: true,
            slowMo: 0,
            devtools: false,
            args
        });
        try{
            //change your credential
            const page = await browser.newPage();
            await page.authenticate({
                username: 'rjd15131gncp356##',
                password: 'EtRrll3CcsXO4CMW'
            });
            await page.emulateTimezone("Asia/Jakarta");
        
            await page.setDefaultNavigationTimeout(0);
            await page.goto(url,{waitUntil: "networkidle2"})
            try{
                await page.waitForSelector('#movie_player > div.ytp-cued-thumbnail-overlay > button',{visible:true ,timeout:30000})
                await page.click('#movie_player > div.ytp-cued-thumbnail-overlay > button')
                console.log('Play')
            }
            catch{
                console.log('Checked')
            }
        }
        catch{
            console.log('View pass')
            await browser.close();
        }    
    }
 
})();
