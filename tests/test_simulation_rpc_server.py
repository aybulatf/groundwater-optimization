import asyncio
from aio_pika import connect_robust
from aio_pika.patterns import RPC


async def main(request_data):
    connection = await connect_robust(
        host='localhost',
        port=5672,
        login='inowas_user',
        password='inowas_password',
        virtualhost='inowas_vhost'
    )

    # Creating channel
    channel = await connection.channel()

    rpc = await RPC.create(channel)

    response = await rpc.proxy.process(content=request_data)

    await connection.close()

    return response


objects_data = [
    {
        "id": 0,
        "type": "well",
        "position": {
            "row": {
                "min": 30,
                "max": 150,
                "result": 100
            },
            "col": {
                "min": 30,
                "max": 150,
                "result": 100
            },
            "lay": {
                "min": 0,
                "max": 0,
                "result": 0
            }
        },
        "flux": {
            "0": {
                "min": 720,
                "max": 720,
                "result": 720
            }
        },
        "concentration": {
            "0": {
                "component1": {
                    "min": 0,
                    "max": 0,
                    "result": 0
                }
            }
        }
    },
    {
        "id": 1,
        "type": "well",
        "position": {
            "row": {
                "min": 30,
                "max": 150,
                "result": 110
            },
            "col": {
                "min": 30,
                "max": 150,
                "result": 110
            },
            "lay": {
                "min": 0,
                "max": 0,
                "result": 0
            }
        },
        "flux": {
            "0": {
                "min": 720,
                "max": 720,
                "result": 720
            }
        },
        "concentration": {
            "0": {
                "component1": {
                    "min": 0,
                    "max": 0,
                    "result": 0
                }
            }
        }
    }
]
request_data1 = {
    'simulation_id': 'test_simulaion1',
    'objects_data': objects_data,
    'optimization_id': 'test_optimization_problem'
}
request_data2 = {
    'simulation_id': 'test_simulaion2',
    'objects_data': objects_data,
    'optimization_id': 'test_optimization_problem'
}
request_data3 = {
    'simulation_id': 'test_simulaion3',
    'objects_data': objects_data,
    'optimization_id': 'test_optimization_problem'
}
request_data4 = {
    'simulation_id': 'test_simulaion4',
    'objects_data': objects_data,
    'optimization_id': 'test_optimization_problem'
}
if __name__ == "__main__":
    import time
    

    loop = asyncio.get_event_loop()

    tasks = [
        loop.create_task(
            main(request_data1)
        ),
        loop.create_task(
            main(request_data2)
        ),
        loop.create_task(
            main(request_data3)
        ),
        loop.create_task(
            main(request_data4)
        )
    ]

    start=time.time()
    fitnesses = loop.run_until_complete(asyncio.gather(*tasks))
    print(time.time()-start)
    print(fitnesses)