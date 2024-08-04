from pprint import pprint
from s3py import * #, ParamType #, Group


#### Create some Params and Systems ####
my_sys = Sys  (None, "my")
my_bol = ParamBool(my_sys, "bol", True)
my_int = ParamU32(my_sys, "int", 123)
my_flt = ParamF32(my_sys, "flt", 4.20)
my_str = ParamStr(my_sys, "str", "Hi, Im libs3!")


# Get the value of a Param
value = my_int.get()
print(f"Param {my_int.name} is {value}")

# Set the value of a Param
my_int.set(456)
print(f"Param {my_int.name} is {my_int.get()}")



#### Create a hierarchical structure of Sys and Params ####
adcs             = Sys      (None,        "adcs")
adcs_status      = ParamU8  (adcs,        "stat", 1)
adcs_error       = ParamBool(adcs,       "err",  False)
adcs_wheel1      = Sys     (adcs,        "whl1")
adcs_wheel1_volt = ParamF32(adcs_wheel1, "volt", 0.0)
adcs_wheel1_rpm  = ParamF32(adcs_wheel1, "rpm",  0.0)
adcs_wheel2      = Sys     (adcs,        "whl2")
adcs_wheel2_volt = ParamF32(adcs_wheel2, "volt", 0.0)
adcs_wheel2_rpm  = ParamF32(adcs_wheel2, "rpm",  0.0)
adcs_wheel3      = Sys     (adcs,         "whl3")
adcs_wheel3_volt = ParamF32(adcs_wheel3, "volt", 0.0)
adcs_wheel3_rpm  = ParamF32(adcs_wheel3, "rpm",  0.0)

adcs_power       = Sys     (adcs,         "pwr")
adcs_power_lim   = Sys     (adcs_power,   "lim")
adcs_power_lim_volt = ParamF32(adcs_power_lim, "volt", 10)
adcs_power_lim_cur  = ParamF32(adcs_power_lim, "cur",  2)


# Alternative access to the nested Params
print(f"ADCS status is: {adcs['stat']}")


# Also possible to set the value
adcs["whl2"]["volt"].set(8.2)
adcs["whl3"]["volt"].set(8.1)


# Print the whole collection
print("\nADCS Param structure:")
adcs.pprint()




#### Get values as dict ####
new_values = {"stat": 2, "whl1":{"volt": 5.0}, "whl2":{"volt": 6.0}, "whl3":{"volt": 7.0}}
adcs.set(new_values)


print("\nadcs sys as dict:")
pprint(adcs.to_dict())




#### Create a Group of Params ####
# Usefully to represent Domain-related groups of Params
wheel_volt = Group("volt",[ # Provide a name  
                adcs_wheel1_volt,
                adcs_wheel2_volt,
                adcs_wheel3_volt
                ])

# Print the whole collection
print("\nVolt of all wheels:")
wheel_volt.pprint()



# Every top-level system (system without a parent) is automatically 
# registered into a local data base: the ParamDB singleton class.
db = ParamDB()

print("\nPrint everything:")
db.print_tree()


print("\nAlso existing groups:")
db.pprint_groups()


# The ParamDB works as an interface to the outside. It provide means to query
# Params.
print(f"\nadcs:whl3:volt is {db.search_param(NamePath('adcs:whl3:volt')).get()}")

# ParamDB can create new Params and Systems at runtime based on a dictionary
# specification
db.spawn_from_dict({"sys": "dict", 
                                 "params": [{"param":"one", "type": "i32", "default": "123" }], 
                                 "subsys": [
                                     {"sys": "sub",
                                      "params":[{"param":"two", "type": "str", "size": 10, "default": "Hohoho" }]}
                                 ]})



# #### Serialization ####

# # Serialize a Collection
# print("\nCollection to a JSON string:")
# print(JsonParamEncoder().encode(adcs))

# # Deserialize a Collection
# print("\nLoad a JSON string to a Collection:")
# json_str = '{"stat": 3,  "whl1": {"volt": 8.0, "rpm": 100}, "whl2": {"volt": 8.2, "rpm": 95}, "whl3": {"volt": 8.1, "rpm": 90}}'
# JsonParamDecoder().decode(adcs, json_str)
# pprint(adcs)

# # Serialize a Group
# print("\n\nGroup to a JSON string:")
# print(JsonParamEncoder().encode(wheel_volt))

# # Deserialize a Group
# print("\nLoad a JSON string to a Group:")
# json_str = '{"whl1": 5.6, "whl2": 2.1, "whl3": 8.0}'
# JsonParamDecoder().decode(wheel_volt, json_str)
# pprint(wheel_volt)