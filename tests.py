# Imports, sorted alphabetically.

# Python packages
import random
import unittest

# Third-party packages
# Nothing for now...

# Modules from this project
import globals as G
from inventory import Inventory
from items import ItemStack
import entity
from . import *

__all__ = (
    'InventoryTests',
)


class InventoryTests(unittest.TestCase):

    def test_init(self):
        for size in [0, 9, random.randint(3, 100)]:
            inv = Inventory(slot_count=size)
            self.assertEqual(inv.slot_count, size)
            self.assertEqual(inv.slots, [None] * size)

    def test_find_empty_slot(self):
        for size in [0, 9, random.randint(3, 100)]:
            inv = Inventory(slot_count=size).find_empty_slot()
            self.assertEqual(inv, 0 if size > 0 else -1)

    def test_add_1(self):
        for size in [0, 9, random.randint(3, 100)]:
            inv = Inventory(slot_count=size)
            item = random.choice(list(G.ITEMS_DIR.keys()))
            block = random.choice(list(G.BLOCKS_DIR.keys()))
            result = inv.add_item(item)
            result2 = inv.add_item(block)
            if size == 0:
                self.assertFalse(result)
                self.assertFalse(result2)
            else:
                self.assertTrue(result)
                self.assertTrue(result2)
                foundItem = False
                foundBlock = False
                for slot in inv.slots:
                    if slot:
                        if slot.type == item and slot.amount == 1:
                            foundItem = True
                        elif slot.type == block and slot.amount == 1:
                            foundBlock = True
                self.assertTrue(foundItem)
                self.assertTrue(foundBlock)
            self.assertEqual(result, result2)

    def test_add_2(self):
        inv = Inventory(slot_count=20)
        block = random.choice(list(G.BLOCKS_DIR.keys()))
        max_items = G.BLOCKS_DIR[block].max_stack_size * 20
        for i in range(0, max_items):
            self.assertTrue(inv.add_item(block))
        item = random.choice(list(G.ITEMS_DIR.keys()))
        inv2 = Inventory(slot_count=20)
        max_items2 = G.ITEMS_DIR[item].max_stack_size * 20
        for i in range(0, max_items2):
            self.assertTrue(inv2.add_item(item))
        self.assertNotIn(None, inv.slots)
        self.assertNotIn(None, inv2.slots)
        for slot in inv.slots:
            self.assertEqual(slot.type, block)
            self.assertEqual(slot.amount, G.BLOCKS_DIR[block].max_stack_size)
        for slot in inv2.slots:
            self.assertEqual(slot.type, item)
            self.assertEqual(slot.amount, G.ITEMS_DIR[item].max_stack_size)

    def test_remove(self):
        inv = Inventory(slot_count=20)
        block = random.choice(list(G.BLOCKS_DIR.keys()))
        max_items = G.BLOCKS_DIR[block].max_stack_size * 20
        for i in range(0, max_items):
            self.assertTrue(inv.add_item(block))
        self.assertFalse(inv.remove_item(block, quantity=0))
        for i in range(0, 20):
            self.assertTrue(inv.remove_item(block, quantity=G.BLOCKS_DIR[block].max_stack_size))
        self.assertEqual(inv.slots, [None] * 20)
        for i in range(0, max_items):
            self.assertTrue(inv.add_item(block))
        for i in range(0, 20):
            self.assertTrue(inv.remove_by_index(i, quantity=G.BLOCKS_DIR[block].max_stack_size))
        self.assertEqual(inv.slots, [None] * 20)
        for i in range(0, 20):
            inv.slots[i] = ItemStack(block, amount=1)
            inv.slots[i].change_amount(-1)
        inv.remove_unnecessary_stacks()
        self.assertEqual(inv.slots, [None] * 20)


class EntityTests(unittest.TestCase):
    def __init__(self,  *args, **kwargs):
        super(EntityTests, self).__init__(*args, **kwargs)
        self.entity_manager = entity.EntityManager()
        self.entity_manager.add_entity(entity.Entity((0, 0, 0), (0, 0)))

    def test_entity(self):
        """
        Creates an entity
        :return: None
        """
        ent = entity.Entity((0, 0, 0), (0, 0))
        self.assertTrue(isinstance(ent, entity.Entity))

    def test_entity_manager(self):
        """
        Creates a entity manager
        :return: None
        """
        entity_manager = entity.EntityManager()
        self.assertTrue(isinstance(entity_manager, entity.EntityManager))

    def test_add_entity(self):
        """
        Adds an entity to the entity manager
        :return:
        """
        ent = entity.Entity((0, 0, 0), (0, 0))
        result = self.entity_manager.add_entity(ent)
        self.assertTrue(result)

    def test_broadcast(self):
        result = self.entity_manager.broadcast(entity.MSG_PICKUP)
        self.assertTrue(result)

    def test_send_message(self):
        result = self.entity_manager.send_message(1, entity.MSG_PICKUP)

        self.assertTrue(result)



if __name__ == '__main__':
    unittest.main()
