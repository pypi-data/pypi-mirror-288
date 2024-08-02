class Precise:
    def __init__(self, decimals):
        self.decimals = decimals
        
    @property
    def precision(self):
        precision = "1"
        for i in range(self.decimals):
            precision += "0"
        return int(precision)
        
    def add(
        self, 
        value1: float, 
        value2:float,
        string: bool = False
    ):
        result = (
            (value1*self.precision) 
            + (value2*self.precision)
        ) / self.precision 
        return result if not string else f"{result:.8f}"
            
    def sub(
        self, 
        value1: float, 
        value2:float,
        string: bool = False
    ):
        result = (
            (value1*self.precision) 
            - (value2*self.precision)
        ) / self.precision 
        return result if not string else f"{result:.8f}"
            
    @classmethod
    def simple3(self, value, total):
        return value*100/total
    
    
    @classmethod
    def get_peŕcentages(self, object):
        
        if type(object) not in [dict, list]:
            raise TypeError
            
            
        if type(object) == dict:
            return self.get_peŕcentages_dict(object)
        else:
            return self.get_peŕcentages_list(object)
            
    @classmethod
    def get_peŕcentages_list(self, object):
        counted = self.list_to_dict(object)
        total = sum(counted.values())
        results = {
            k: self.simple3(v, total) for k, v in counted.items()
        }
        return results
        
    @classmethod    
    def get_peŕcentages_dict(self, my_dict):
        total = sum(my_dict.values())
        results = {
            k: self.simple3(v, total) for k, v in my_dict.items()
        }
        return results
        
    @classmethod
    def list_to_dict(self, my_list):
        results = {}
        
        for i in my_list:
            if i not in results.keys():
                results[i] = 1
            else:
                results[i] += 1
        return results
        
            
            
