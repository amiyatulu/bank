import simpy
import csv

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
        print("%s deposited %d at time %d" % (self.name, self.amount_deposited, self.env.now))
        print("amount left in container is % d at time %d" % (self.money_container.level, self.env.now))
        yield self.env.timeout(self.wait_time)
        yield self.money_container.get(self.amount_withdrawn)
        print("%s withdrawn %d at time %d" % (self.name, self.amount_withdrawn, self.env.now))
        print("amount left in container is % d at time %d" % (self.money_container.level, self.env.now))


if __name__ == "__main__":
    env = simpy.Environment()
    cont = simpy.Container(env)
    with open("data.csv", newline="") as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            x = Person_Transaction(env, name= row["Name"], money_container=cont, time_of_deposit=int(row["Time of Deposit"]), time_of_withdraw=int(row["Time of Withdraw"]), amount_deposited=int(row["Amount Deposited"]), amount_withdrawn=int(row["Amount Withdrawn"]))
    env.run(until=20)
