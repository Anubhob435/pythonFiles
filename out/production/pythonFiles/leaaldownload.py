def wait_for_results_and_download_judgments(driver):
    try:
        print("Waiting for results to load...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "showList"))
        )
        time.sleep(2)

        # Collect judgment links
        show_list_div = driver.find_element(By.ID, "showList")
        rows = show_list_div.find_elements(By.TAG_NAME, "tr")

        print("Collecting all the links for only Judgments(not for orders)")

        judgment_links = []
        for row in rows:
            links = row.find_elements(By.TAG_NAME, "a")
            for link in links:
                if link.text.strip().lower() == "judgment":
                    href = link.get_attribute("href")
                    if href:
                        judgment_links.append(href)

        print(f"Found {len(judgment_links)} judgment link(s).")

        for i, pdf_url in enumerate(judgment_links, 1):
            print(f"Downloading judgment #{i}")
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(pdf_url)
            time.sleep(5)  # Allow time for download
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            time.sleep(1)

        print(f"All available judgments downloaded: {len(judgment_links)}")
    except Exception as e:
        print(f"Error while fetching judgments: {e}")