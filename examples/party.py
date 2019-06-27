#!/usr/bin/env python
'''
This module has the example for usecase of Assembly and Pipelines.

This shows a simple example of preparing multiple recipe(s) for a party.
- It assumes there is a menu of (1) Tea, (2) Rice, (3) Pizza and (4) Curry.
- All the 4 dishes on the menu have different recipe so there will be an
  individual pipeline for each dish that executes the recipe in serial order.
- Top level Assembly, "Party", will have these 4 pipelines that can be
  executed in parallel.
'''


import time

from src import pipeline 
from src import logger
from src import task
from src import worker


log = logger.getLogger(__name__)

class DemoStage(pipeline.Stage):

    def run(self, data):
        log.info("Performing : %s ", self.name)
        time.sleep(2)

class MyAssembly(pipeline.Assembly):

    def _run(self):
        with worker.ThreadPool(2) as tpool:
            for pipeline in self.pipelines:
                tpool.append_task(pipeline)

def demo():

    p_tea = pipeline.Pipeline("Tea")
    p_tea.stages.append(DemoStage("Boil Water"))
    p_tea.stages.append(DemoStage("Grate Ginger"))
    p_tea.stages.append(DemoStage("Add Tea Leaves"))
    p_tea.stages.append(DemoStage("Add milk"))
    p_tea.stages.append(DemoStage("Boil Tea for 10 minutes."))


    p_rice = pipeline.Pipeline("Rice")
    p_rice.stages.append(DemoStage("Soak Rice for 10 minutes."))
    p_rice.stages.append(DemoStage("Wash Rice"))
    p_rice.stages.append(DemoStage("Boil Water"))
    p_rice.stages.append(DemoStage("Add Rice"))
    p_rice.stages.append(DemoStage("Boil Rice for 10 minutes."))

    p_pizza  = pipeline.Pipeline("Pizza")
    p_pizza.stages.append(DemoStage("Ferment dough for 4 hours."))
    p_pizza.stages.append(DemoStage("Roll dough."))
    p_pizza.stages.append(DemoStage("Add sauce"))
    p_pizza.stages.append(DemoStage("Add toppings"))
    p_pizza.stages.append(DemoStage("Bake 10 minutes"))
    p_pizza.stages.append(DemoStage("Remove baking plate."))
    p_pizza.stages.append(DemoStage("Bake 15 minutes"))


    # import pdb ; pdb.set_trace()
    # p_tea.run()
    # p_rice.run()
    # p_pizza.run()

    # return

    party = MyAssembly(name='party')
    party.pipelines.extend([p_tea, p_rice, p_pizza])
    party.run()

if __name__ == '__main__':

    demo()
