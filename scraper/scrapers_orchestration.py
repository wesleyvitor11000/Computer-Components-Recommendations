from VersusScraper import VersusScraper
from VersusData import data_to_colect_by_comp_type

import os
import json
import pandas as pd
import copy
from tqdm import tqdm
import time
import random


def main():
    ignore_saveds = True
    comps_infos_dir = "res/components/"

    os.makedirs(comps_infos_dir, exist_ok=True)

    for c in data_to_colect_by_comp_type.keys():
        base_infos_file = f"{comps_infos_dir}/{c}_base_infos_versus.json"
        component_type_scraper = VersusScraper(f"https://versus.com/en/{c}")

        if os.path.exists(base_infos_file) and ignore_saveds:
            print(f"Ignoring base informations collection for {c}.")
            base_comp_infos_fl = open(base_infos_file)
            base_comp_infos = json.load(base_comp_infos_fl)
        else:
            print("\n" * 2, "#" * 100)
            print(f"running for {c}")

            base_comp_infos = component_type_scraper.scrape_common_elements(
                explore_pages=True
            )

            with open(base_infos_file, "w") as file:
                json.dump(base_comp_infos, file)


        i = 0
        
        checkpoint_file = f"{comps_infos_dir}/checkpoint_{c}.txt"
        specs_dir = f"{comps_infos_dir}/{c}_specs_versus.json"
        comp_checkpoint = set()
        new_comps = set()
        
        collected_comps = []
        
        if os.path.exists(specs_dir):
            with open(specs_dir, "r") as file:
                collected_comps = json.load(file)
                
        
        if os.path.exists(checkpoint_file):
            with open(checkpoint_file, "r") as file:
                links = file.readlines()
                links = [l[:-1] for l in links]
                comp_checkpoint = set(links)
        
        for component in tqdm(base_comp_infos):
            i += 1
            data_to_colect = data_to_colect_by_comp_type[c].copy()
            comp_link = component["link"]
            
            if len(comp_checkpoint) >= len(base_comp_infos):
                break
            
            if comp_link in comp_checkpoint:
                # print(f"\nignoring {comp_link}")
                continue
            
            new_comps.add(comp_link)

            if "href" in data_to_colect.keys():
                modified_hrefs = copy.deepcopy(data_to_colect["href"])
                for k, v in modified_hrefs.items():
                    modified_hrefs[k][0] = v[0].format(name=comp_link.split("/")[-1])

                data_to_colect["href"] = modified_hrefs

            comp_specific_infos = component_type_scraper.scrape_specific_elements(
                comp_link, data_to_colect
            )
            collected_comps.append(component | comp_specific_infos)

            if i % 5 == 0 or i >= len(base_comp_infos) - 1:
                with open(checkpoint_file, "a")  as file:
                    [file.write(f"{comp}\n") for comp in new_comps]
                
                with open(specs_dir, "w") as file:
                    json.dump(collected_comps, file)
                    
                new_comps = set()

            if i % 50 == 0:
                time.sleep(
                    random.uniform(3, 5)
                )
                
            if i % 250 == 0:
                time.sleep(
                    random.uniform(8, 13)
                )
                
            
        component_type_scraper.close_scraper()

        outp_specs_file = pd.ExcelWriter(f"res/components/{c}_specs_versus.xlsx")
        pd.DataFrame(collected_comps).to_excel(outp_specs_file)
        outp_specs_file.close()


if __name__ == "__main__":
    main()
