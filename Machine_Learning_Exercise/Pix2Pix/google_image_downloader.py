from selenium import webdriver
import time, requests
import base64


def search_google(search_query):
    browser = webdriver.Chrome("./chromedriver")
    search_url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={search_query}"
    images_url = []

    # open browser and begin search
    browser.get(search_url)
    elements = browser.find_elements_by_class_name('rg_i')

    count = 0
    while(count<1000):
        first = True
        for e in elements[count:]:
            # get images source url
            try:
                e.click()
            except:
                pass
                continue
            time.sleep(1)
            element = browser.find_elements_by_class_name('v4dQwb')

            # Google image web site logic
            if first:
                big_img = element[0].find_element_by_class_name('n3VNCb')
                first = False
            else:
               big_img = element[1].find_element_by_class_name('n3VNCb')

            images_url.append(big_img.get_attribute("src"))

            if "base64" in images_url[count]:
                base64_data = images_url[count].split(",")[1]
                # base64_data = 'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAADBQTFRFA6b1q Ci5/f2lt/9yu3 Y8v2cMpb1/DSJbz5i9R2NLwfLrWbw m T8I8////////SvMAbAAAABB0Uk5T////////////////////AOAjXRkAAACYSURBVHjaLI8JDgMgCAQ5BVG3//9t0XYTE2Y5BPq0IGpwtxtTP4G5IFNMnmEKuCopPKUN8VTNpEylNgmCxjZa2c1kafpHSvMkX6sWe7PTkwRX1dY7gdyMRHZdZ98CF6NZT2ecMVaL9tmzTtMYcwbP y3XeTgZkF5s1OSHwRzo1fkILgWC5R0X4BHYu7t/136wO71DbvwVYADUkQegpokSjwAAAABJRU5ErkJggg=='.replace(
                #     ' ', '+')
                imgdata = base64.b64decode(base64_data)
                with open(f"./google_img/search{count + 1}.jpg", "wb") as file:
                    file.write(imgdata)
            else:
                # write image to file
                reponse = requests.get(images_url[count])


                if reponse.status_code == 200:
                    with open(f"./google_img/search{count+1}.jpg","wb") as file:

                        if 'image' not in reponse.headers['Content-Type'] and "base64" in reponse.content:
                            imgdata = base64.b64decode(reponse.content)
                            file.write(imgdata)
                        else:
                            file.write(reponse.content)

            count += 1

            # Stop get and save after 5
            # if count == 5:
            #     break

        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(3)
        elements = browser.find_elements_by_class_name('rg_i')

    return images_url

items = search_google('櫻木花道')

