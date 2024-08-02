from EPCPyYes.core.v1_2 import helpers
from typing import List
import secrets
    
class SerialNumberGenerator:

    def __init__(self,gcp:str, indicator:str,count:str, length:int, sequence_start:str = "0",charset:str = "0", prefix:str = "0", suffix:str = "0", sparseness:str = "0", pack_level:str = "0", item_ref:str = "0") -> None:
        self.gcp = gcp 
        self.count = count
        self.indicator = indicator
        self.length = length
        self.prefix = prefix
        self.suffix = suffix
        self.sparseness = sparseness
        self.pack_level = pack_level
        self.item_ref = item_ref
        self.sequence_start = sequence_start
        self.charset = charset
        if len(self.charset) < 2:
            raise ValueError("More than 2 characters required to generate random serial numbers")

    def __get_serial_numbers_by_length(self, required_length:int) -> List[str]:
        serial_nums = set()
        while len(serial_nums) < int(self.count):
            new_serial = ''.join(secrets.choice(self.charset) for _ in range(required_length))
            serial_nums.add(new_serial)
        return list(serial_nums)

    ## generate sequential numbers with prefix and suffix
    def generate_sequential_numeric_nos(self) -> List[str]:
        if(self.suffix != "0"):
            if len(self.prefix+self.suffix) > self.length:
                raise ValueError("Length of prefix and suffix cannot be equal to length of serial number")
        else:
            if len(self.prefix) > self.length:
                raise ValueError("Length of prefix and suffix cannot be equal to length of serial number")
        final_epcs = []
        if(self.prefix != "0" and self.suffix == "0"):
            start = self.prefix
            first_iteration = True
            while len(start) < self.length:
                if(first_iteration):
                    start+=self.sequence_start
                    first_iteration = False
                else:
                    start+="0"
            end = int(start) + int(self.count)
            nums = range(int(start),int(end))
            list(map(lambda x:final_epcs.append(x), helpers.gtin_urn_generator(self.gcp, self.indicator, self.item_ref, nums)))
        elif(self.suffix != "0" and self.prefix != "0"):
            start = self.prefix
            i = 0
            while i < (self.length - (len(self.prefix) + len(self.suffix))):
                if i == 0:
                    start+=self.sequence_start
                else:
                    start += "0"
                i+=1
            end = int(start)+int(self.count)
            nums = range(int(start), int(end))
            epc_gen = helpers.gtin_urn_generator(self.gcp, self.indicator, self.item_ref, nums)
            list(map(lambda x:final_epcs.append(x), [x+self.suffix for x in epc_gen]))
        return final_epcs
    
    ## generate random numbers with prefix and suffix 
    def generate_random_serial_numbers(self) -> List[str]:
        if self.charset == "0":
            raise ValueError("Provide characters to generate random numbers")   
        final_epcs = []  
        if self.prefix == "0" and self.suffix == "0":
            list(map(lambda x: final_epcs.append(x), [''.join(['urn:epc:id:sgtin:{0}.{1}{2}.'.format(self.gcp, self.indicator, self.item_ref), x]) for x in self.__get_serial_numbers_by_length(self.length)]))
        elif self.prefix != "0" and self.suffix == "0":
            required_length = self.length - len(self.prefix)
            if required_length == 0:
                raise ValueError("Could not generate random serial numbers since length of prefix and suffix equals length of serial number")
            list(map(lambda x: final_epcs.append(x), [''.join(['urn:epc:id:sgtin:{0}.{1}{2}.'.format(self.gcp, self.indicator, self.item_ref), x]) for x in [self.prefix+x for x in self.__get_serial_numbers_by_length(required_length)]]))
        elif self.prefix != "0" and self.suffix != "0":
            required_length = self.length - (len(self.prefix) + len(self.suffix))
            if required_length == 0:
                raise ValueError("Could not generate random serial numbers since length of prefix and suffix equals length of serial number")
            list(map(lambda x: final_epcs.append(x), [''.join(['urn:epc:id:sgtin:{0}.{1}{2}.'.format(self.gcp, self.indicator, self.item_ref), x]) for x in [self.prefix+x+self.suffix for x in self.__get_serial_numbers_by_length(required_length)]]))
        return final_epcs