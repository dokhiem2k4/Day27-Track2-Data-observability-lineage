from playwright.sync_api import sync_playwright

AIRFLOW_URL = "http://localhost:8080"
USER = "admin"
PASS = "admin"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1440, "height": 900})
    page = ctx.new_page()

    # Login
    page.goto(f"{AIRFLOW_URL}/login")
    page.wait_for_load_state("networkidle")
    page.fill("#username", USER)
    page.fill("#password", PASS)
    page.click("[type=submit]")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    print("After login URL:", page.url)

    # 1. DAG list — dùng /home thay vì /dags
    page.goto(f"{AIRFLOW_URL}/home")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(4000)
    print("DAG list URL:", page.url)
    page.screenshot(path="evidence/01_dag_list.png", full_page=True)
    print("01_dag_list.png saved")

    # 2. DAG grid view
    page.goto(f"{AIRFLOW_URL}/dags/sales_data_quality_pipeline/grid")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(5000)
    print("Grid URL:", page.url)
    page.screenshot(path="evidence/02_dag_grid.png", full_page=True)
    print("02_dag_grid.png saved")

    # 3. Task log — success run
    page.goto(f"{AIRFLOW_URL}/log?dag_id=sales_data_quality_pipeline&task_id=validate_orders&execution_date=2026-05-15T07%3A28%3A02%2B00%3A00&map_index=-1")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    page.screenshot(path="evidence/03_task_log_success.png", full_page=True)
    print("03_task_log_success.png saved")

    # 4. Task log — failed run
    page.goto(f"{AIRFLOW_URL}/log?dag_id=sales_data_quality_pipeline&task_id=validate_orders&execution_date=2026-05-15T07%3A28%3A47%2B00%3A00&map_index=-1")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(3000)
    page.screenshot(path="evidence/04_task_log_failed.png", full_page=True)
    print("04_task_log_failed.png saved")

    browser.close()
    print("All screenshots done.")
