# Dictates which parameters are passed into the pytests

def pytest_addoption(parser):
    parser.addoption("--zen_qm", action="store")
    parser.addoption("--zen_asil", action="store")
    parser.addoption("--vcc", action="store")
    parser.addoption("--dbc", action="store")
    parser.addoption("--asc", action="store")
