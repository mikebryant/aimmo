#!/usr/bin/env python

import logging
from pykube import HTTPClient
from pykube import KubeConfig
from pykube import Ingress, ReplicationController, Service
import time

LOGGER = logging.getLogger(__name__)

def create_game_rc(api, name, environment_variables):
    rc = ReplicationController(
        api,
        {
            'kind': 'ReplicationController',
            'apiVersion': 'v1',
            'metadata': {
                'name': "game-%s" % name,
                'namespace': 'default',
                'labels': {
                    'app': 'aimmo-game',
                    'game': name,
                },
            },
            'spec': {
                'replicas': 1,
                'selector': {
                    'app': 'aimmo-game',
                    'game': name,
                },
                'template': {
                    'metadata': {
                        'labels': {
                            'app': 'aimmo-game',
                            'game': name,
                        },
                    },
                    'spec': {
                        'containers': [
                            {
                                'env': [
                                    {
                                        'name': env_name,
                                        'value': env_value,
                                    } for env_name, env_value in environment_variables.items()
                                ],
                                'image': 'ocadotechnology/aimmo-game:latest',
                                'ports': [
                                    {
                                        'containerPort': 5000,
                                    },
                                ],
                                'name': 'aimmo-game',
                            },
                        ],
                    },
                },
            },
        },
    )
    rc.create()


def create_game_service(api, name, _config):
    service = Service(
        api,
        {
            'kind': 'Service',
            'apiVersion': 'v1',
            'metadata': {
                'name': "game-%s" % name,
                'labels': {
                    'app': 'aimmo-game',
                    'game': name,
                },
            },
            'spec': {
                'selector': {
                    'app': 'aimmo-game',
                    'game': name,
                },
                'ports': [
                    {
                        'protocol': 'TCP',
                        'port': 80,
                        'targetPort': 5000,
                    },
                ],
                'type': 'NodePort',
            },
        },
    )
    service.create()


def get_games():
    return {
        'main': {
            'VAR1': 'VAL1',
        }
    }


def maintain_games(api, games):
    for object_type, creation_callback in (
        (ReplicationController, create_game_rc),
        (Service, create_game_service),
    ):
        current_game_names = set()
        for game in object_type.objects(api).filter(selector={'app': 'aimmo-game'}):
            game_name = game.obj['metadata']['labels']['game']
            current_game_names.add(game_name)
            if game_name not in games:
                LOGGER.info("Deleting game %s", game_name)
                game.delete()
        for game_id, game_config in games.items():
            if game_id not in current_game_names:
                LOGGER.info("Creating game %s", game_id)
                creation_callback(api, game_id, game_config)
    ingress = Ingress(
        api,
        {
            'apiVersion': 'extensions/v1beta1',
            'kind': 'Ingress',
            'metadata': {
                'name': 'game',
            },
            'spec': {
                'rules': [
                    {
                        'host': 'aimmo.hostname',
                        'http': {
                            'paths': [
                                {
                                    'path': "/game/%s/" % name,
                                    'backend': {
                                        'serviceName': "game-%s" % name,
                                        'servicePort': 5000,
                                    },
                                } for name in games.keys()
                            ],
                        },
                    },
                ],
            },
        },
    )
    if ingress.exists():
        ingress.update()
    else:
        ingress.create()


def main():
    logging.basicConfig(level=logging.DEBUG)
    api = HTTPClient(KubeConfig.from_service_account())
    while True:
        games = get_games()
        maintain_games(api, games)
        time.sleep(5)


if __name__ == '__main__':
    main()
