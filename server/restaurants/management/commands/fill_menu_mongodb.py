from typing import Any
from django.core.management.base import BaseCommand
from restaurants.models import Menu, MenuItem, MenuCategory
import json
import os
import time

class Command(BaseCommand):
    help="Sends the bulk of documents, in mongoDB collection"
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        
        path_till_server = os.getcwd()
        json_l_path = os.path.join(path_till_server, "data", "menu-items-data-600-rest-global-uuid-digitalOcean.jsonl")
        
        BULK_MENU_QUERIES: list[Menu] = []
        
        start_time = time.time()
        
        with open(json_l_path, "r") as fp:
            self.stdout.write(f"Loaded {json_l_path} file.... starting to build BULK QUERY")    
            for line in fp:
                
                try:
                    restaurant_data = json.loads(line)
                    restaurant_id = restaurant_data.get("restaurant_uuid")
                    
                    if "menu" not in restaurant_data:
                        continue
                        
                    menu_data = restaurant_data["menu"]
                    
                    if isinstance(menu_data, dict):
                        mc_list: list[MenuCategory] = []
                        
                        for category_name, menu_items in menu_data.items():
                            mi_list: list[MenuItem]= []
                            
                            if isinstance(menu_items, dict):
                            
                                for menu_name, data in menu_items.items():
                                    
                                    
                                    if isinstance(data, dict):
                                        # The data only contains "Veg" and "Non-veg", not "Egg" that's why only including this.
                                        food_type = "V" if data.get("veg_or_non_veg") == "Veg" else "NV"
                                        
                                        mi = MenuItem(
                                            name=menu_name,
                                            price=float(data.get("price", 0.0)),
                                            food_type=food_type,
                                            image_url=data.get("image", ""),
                                        )
                                        
                                        mi_list.append(mi)
                                    
                                mc = MenuCategory(
                                    name=category_name,
                                    menu_items=mi_list,
                                )
                                
                                mc_list.append(mc)
                                
                        m = Menu(
                            restaurant_id=restaurant_id,
                            categories=mc_list,
                        )
                        
                        BULK_MENU_QUERIES.append(m)
                                         
                except Exception as e:
                    print(e)
          
        
        if BULK_MENU_QUERIES:
            
            try:
                self.stdout.write(f"Inserting {len(BULK_MENU_QUERIES)} menu documents into MongoDB...")
                
                Menu.objects.insert(BULK_MENU_QUERIES, load_bulk=False)
                
                
                self.stdout.write(self.style.SUCCESS("Successfully inserted all the menu data!!!"))
                
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Exception: {e}"))
                
                
            finally:
                end_time = time.time()
                self.stdout.write(self.style.SUCCESS(f"EXECUTION TIME: {end_time - start_time}"))
                
        