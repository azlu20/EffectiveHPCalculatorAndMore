from PullChampionStats import *
import csv
import pandas as pd
from GetItems import *
import matplotlib.pyplot as plt
import numpy as np


class CalculationMachine(object):
    def __init__(self, champion, level=1, items=[]):
        # champion logic
        self.champion = champion
        self.level = level
        self.champion_filename = create_file()
        self.champion_dataset = pd.read_csv(self.champion_filename, sep=",", header=0)
        self.championdata = self.champion_dataset["Name"].searchsorted(self.champion, "left")

        # item logic
        self.item_filename = item_create_file()
        self.item_dataset = pd.read_csv(self.item_filename, sep=",", header=0)
        self.item_dataset = self.item_dataset.sort_values("Name")
        self.items = items

        # Setting baseline gold efficiency value
        itemdata = int(self.item_dataset["Name"].searchsorted("Ruby Crystal", "left"))
        self.hp_per_gold = float(self.item_dataset.iloc[itemdata]["Health"]) / float(
            self.item_dataset.iloc[itemdata]["Gold"])
        itemdata = int(self.item_dataset["Name"].searchsorted("Cloth Armor", "left"))
        self.armor_per_gold = float(self.item_dataset.iloc[itemdata]["Armor"]) / float(
            self.item_dataset.iloc[itemdata]["Gold"])
        itemdata = int(self.item_dataset["Name"].searchsorted("Null-Magic Mantle", "left"))
        self.mr_per_gold = float(self.item_dataset.iloc[itemdata]["Magic Resist"]) / float(
            self.item_dataset.iloc[itemdata]["Gold"])
        self.calculateBaseStats()

        #string search setup
        firstrow = "-qwertyuiop"
        secondrow = "asdfghjkl;'"
        thirdrow = "zxcvbnm,./ "
        self.qwertydict = {}
        count = 0
        for ele in firstrow:
            self.qwertydict[ele] = (0, count)
            count+=1
        count = 0
        for ele in secondrow:
            self.qwertydict[ele] = (0, count)
            count+=1
        count = 0
        for ele in thirdrow:
            self.qwertydict[ele] = (0, count)
            count+=1
    def changeChampion(self, champion):
        self.champion = champion
        self.calculateBaseStats()

    def changeLevel(self, level):
        self.level = level
        self.calculateBaseStats()

    def changeItems(self, items):
        self.items = items
        self.calculateBaseStats()

    def calculateBaseStats(self):
        # champion level calculations
        self.hp = float(self.champion_dataset.iloc[self.championdata]["HP"]) + float(
            self.level * self.champion_dataset.iloc[self.championdata]["HP Per Level"])
        self.armor = float(self.champion_dataset.iloc[self.championdata]["Armor"]) + float(
            self.level * self.champion_dataset.iloc[self.championdata]["Armour Per Level"])
        self.mr = float(self.champion_dataset.iloc[self.championdata]["Spell Block"]) + float(
            self.champion_dataset.iloc[self.championdata]["Spell Block Per Level"])
        # item calculations
        for item in self.items:
            itemdata = int(self.item_dataset["Name"].searchsorted(item, "left"))
            self.hp += float(self.item_dataset.iloc[itemdata]["Health"])
            self.armor += float(self.item_dataset.iloc[itemdata]["Armor"])
            self.mr += float(self.item_dataset.iloc[itemdata]["Magic Resist"])

    def hpOrResistances(self):
        # Calculating Which To Use
        hp_effective_hp_per_gold_ad = (self.hp_per_gold) * (100 + self.armor) / 100
        hp_effective_hp_per_gold_ap = (self.hp_per_gold) * (100 + self.mr) / 100

        armor_effective_hp_per_gold = self.hp * (self.armor_per_gold) / 100
        mr_effective_hp_per_gold = self.hp * (self.mr_per_gold) / 100
        print(
            "Health is more effective against AD opponents" if hp_effective_hp_per_gold_ad > armor_effective_hp_per_gold else "Armor more effective at these breakpoints against AD enemies")
        print(
            "Health is more effective against AP opponents" if hp_effective_hp_per_gold_ap > mr_effective_hp_per_gold else "MR more effective at these breakpoints against AP enemies")

    def printEffectiveHPGained(self, gold):
        print(f"Armor: Expect around {self.hp * self.armor_per_gold / 100 * gold} effective HP for {gold}G amount")
        print(f"Magic Resist: Expect around {self.hp * self.mr_per_gold / 100 * gold} effective HP for {gold}G amount")
        print(
            f"Health: Expect around {(self.hp_per_gold * gold) * (100 + self.armor) / 100} effective HP for {gold}G "
            f"amount")

    def compareReasonableItems(self, item):
        try:
            # three logn searches instead of an n search and logn search
            itemdata = self.item_dataset["Name"].searchsorted(item, "left")
            goldval = float(self.item_dataset.iloc[itemdata]["Gold"])

            eff_hp_ad, eff_hp_ap = self.calculateItemTankGoldEfficiency(item)
            gold_sorted = self.item_dataset.sort_values("Gold")
            goldindex = gold_sorted["Gold"].searchsorted(goldval, "left")
            max_eff_hp_ad = eff_hp_ad
            max_eff_hp_ad_name = item
            max_eff_hp_ap = eff_hp_ap
            max_eff_hp_ap_name = item
            for i in range(goldindex-5, goldindex+5):
                name = str(gold_sorted.iloc[i]["Name"])
                new_hp_ad, new_hp_ap = self.calculateItemTankGoldEfficiency(name)
                if(new_hp_ad > max_eff_hp_ad):
                    max_eff_hp_ad = new_hp_ad
                    max_eff_hp_ad_name = name
                if(new_hp_ap > max_eff_hp_ap):
                    max_eff_hp_ap = new_hp_ap
                    max_eff_hp_ap_name = name

            return max_eff_hp_ad_name, max_eff_hp_ap_name

        except:
            print("caught exception")

    def calculateItemTankGoldEfficiency(self, item, printFlag=False):
        itemdata = self.item_dataset["Name"].searchsorted(item, "left")
        goldval = float(self.item_dataset.iloc[itemdata]["Gold"])
        hp = float(self.item_dataset.iloc[itemdata]["Health"])
        armor = float(self.item_dataset.iloc[itemdata]["Armor"])
        mr = float(self.champion_dataset.iloc[self.championdata]["Spell Block"])
        effective_hp_ad = self.hp * armor / 100 + (100 + self.armor) / 100 * hp + armor / 100 * hp
        effective_hp_ap = self.hp * mr / 100 + (100 + self.mr) / 100 * hp + mr / 100 * hp
        if printFlag:
            print(f"Effective HP against AD gained from this item is {effective_hp_ad}")
            print(f"Effective HP against AP gained from this item is {effective_hp_ap}")
            # Assuming equal weight onto ad and ap
            print(
                f"One Gold would net you {((effective_hp_ad + effective_hp_ap) / 2) / goldval} Effective HP with this "
                f"item at this breakpoint")
            print(
                f"To compare, based on the Ruby Crystal Rate, one gold would net you {(self.hp_per_gold * (100 + self.armor) / 100 + self.hp_per_gold * (100 + self.mr) / 100) / 2} Effective HP")
        return effective_hp_ad, effective_hp_ap

    def SSEStringSearch(self, string):
        test = (self.item_dataset["Name"].searchsorted(string, "left"))
        if(test < self.item_dataset.count(0)[0]):
            return True
        min = 9999
        min_name = None
        for ele in self.item_dataset["Name"]:
            val = self.calculateDistance(string.lower(), ele.lower())
            if(val < min):
                min = val
                min_name = ele
        print(min)
        return min_name
    def calculateDistance(self, word1, word2):
        i = 0
        val = 0
        while i < len(word1):
            if(i < len(word2)):
                x1, y1 = self.qwertydict[word1[i]]
                x2, y2 = self.qwertydict[word2[i]]
                if(x1 == x2 and y1 == y2):
                    val -= 1
                val += 0.5 * ((x1 - x2)**2 + (y1-y2)**2)
            else:
                val += 1
            i+=1
        return val
    def calculateHeartSteel(self, xProcs):
        self.changeItems(["Heartsteel"])
        procs = np.array(range(1, 1000))
        hp_values = np.zeros(len(procs))
        health_gained = np.zeros(len(procs))
        for idx, i in enumerate(procs):
            cur_gained = 12.5 + 0.006 * self.hp
            self.hp += cur_gained
            hp_values[idx] = self.hp+cur_gained
            health_gained[idx] = cur_gained
        plt.plot(procs, health_gained)
        plt.show()
        print(f"At {xProcs} procs, {self.champion} would have {hp_values[xProcs]} with {np.sum(health_gained[0:xProcs])} health gained from HeartSteel passive.")

newcalc = CalculationMachine("Vayne", 11, [])
# newcalc.hpOrResistances()
newcalc.calculateHeartSteel(100)