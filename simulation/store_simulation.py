import simpy

def run_simulation(allocation):
    env = simpy.Environment()
    output = []

    def customer_flow(env, product, qty):
        for _ in range(int(qty)):
            yield env.timeout(1)
            output.append((env.now, product))

    for product, qty in allocation.items():
        env.process(customer_flow(env, product, qty))

    env.run()
    return output
