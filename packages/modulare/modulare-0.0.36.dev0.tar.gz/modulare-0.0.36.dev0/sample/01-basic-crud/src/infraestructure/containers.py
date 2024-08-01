from dependency_injector import containers, providers

class AppContainer(containers.DynamicContainer):
    config = providers.Configuration()