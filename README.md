# Druhy_ukol_2
Přepracován kód "doplneni_task_manager-2
Přepracován kód "test_task_manager"
Výsledky po stuštění testovacího souboru:
=============================================================================================================== test session starts ================================================================================================================
platform win32 -- Python 3.13.2, pytest-8.3.5, pluggy-1.5.0 -- C:\Users\Petr\AppData\Local\Programs\Python\Python313\python.exe
cachedir: .pytest_cache
metadata: {'Python': '3.13.2', 'Platform': 'Windows-11-10.0.26100-SP0', 'Packages': {'pytest': '8.3.5', 'pluggy': '1.5.0'}, 'Plugins': {'anyio': '4.9.0', 'asyncio': '1.0.0', 'base-url': '2.1.0', 'cov': '6.1.1', 'html': '4.1.1', 'metadata': '3.1.1', 'playwright': '0.7.0'}, 'Base URL': ''}
rootdir: C:\Users\Petr\Documents\Testování\Projekt 2
plugins: anyio-4.9.0, asyncio-1.0.0, base-url-2.1.0, cov-6.1.1, html-4.1.1, metadata-3.1.1, playwright-0.7.0
asyncio: mode=Mode.STRICT, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 6 items                                                                                                                                                                                                                                   

test_task_manager.py::test_pridat_ukol_valid PASSED                                                                                                                                                                                           [ 16%]
test_task_manager.py::test_pridat_ukol_empty_nazev PASSED                                                                                                                                                                                     [ 33%] 
test_task_manager.py::test_aktualizovat_ukol_valid PASSED                                                                                                                                                                                     [ 50%]
test_task_manager.py::test_aktualizovat_ukol_invalid_stav PASSED                                                                                                                                                                              [ 66%] 
test_task_manager.py::test_odstranit_ukol_valid PASSED                                                                                                                                                                                        [ 83%]
test_task_manager.py::test_odstranit_ukol_invalid_id PASSED                                                                                                                                                                                   [100%] 

================================================================================================================ 6 passed in 0.17s =================================================================================================================
