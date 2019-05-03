class Seq:
    def __init__(self, strbases):   #SIEMPRE
        self.strbases = strbases

    def len(self):
        return len(self.strbases)

    def complement(self):
        empty = ""
        for letter in self.strbases:
            if letter == "A":
                empty += "T"
            if letter == "T":
                empty += "A"
            if letter == "G":
                empty += "C"
            if letter == 'C':
                empty += "G"
        return Seq(empty)   #here i've created an object

    def reverse(self):
        return Seq(self.strbases[::-1])

    def count(self, base):
        result = 0
        for e in self.strbases:
            if e == base:
                result += 1
        return result

    def perc(self, base):
        return self.count(base)*100/self.len()
