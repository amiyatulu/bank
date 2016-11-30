import simpy

class Person_Transaction(object):
    def __init__(self, env, name, money_container, time_of_deposit, time_of_withdraw, amount_deposited, amount_withdrawn):
        self.env = env
        self.name = name
        self.money_container = money_container
        self.time_of_deposit = time_of_deposit
        self.wait_time = time_of_withdraw - time_of_deposit
        self.amount_deposited = amount_deposited
        self.amount_withdrawn = amount_withdrawn
        self.action = env.process(self.run())


    def run(self):
        yield self.env.timeout(self.time_of_deposit)
        yield self.money_container.put(self.amount_deposited)
        print("%s deposited at time %d" % (self.name, self.env.now))
        print("container level after %s deposited is % d" % (self.name, self.money_container.level))
        yield self.env.timeout(self.wait_time)
        yield self.money_container.get(self.amount_withdrawn)
        print("%s withdrawn at time %d" % (self.name, self.env.now))
        print("container level after %s has withdrawn is % d" % (self.name, self.money_container.level))


if __name__ == "__main__":
    env = simpy.Environment()
    cont = simpy.Container(env)
    person1 = Person_Transaction(env, name="Amiya", money_container=cont, time_of_deposit=2, time_of_withdraw=4, amount_deposited=50, amount_withdrawn=40)
    person2 = Person_Transaction(env, name="Sourav", money_container=cont, time_of_deposit=3, time_of_withdraw=4, amount_deposited=100, amount_withdrawn=500)
    env.run(until=15)
