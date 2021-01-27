import numpy as np
class LCG(object):
    """
    Linear Conguential Generatro
    """
    # i think i need initial the seed and provide a defulat value
    X0 = 0
    def __init__(self):
        """

        :param seed: X0 is the seed
        :param multiplier: a is called multiplier, 0<a<M
        :param increment: c is called increment, 0<c<=M
        :param modulus:M is the modulus which is also the maximum range of this sequence
        """
        self.seed = np.int64(1)
        self.multiplier = np.int64(1103515245)
        self.increment = np.int64(12345)
        # modulus(M) represent the int32 max limitation, so we need use int64 to initial Mb
        self.modulus = np.power(2, 32, dtype=np.int64)
        print(f"Our initial parameters: seed(X0) = {self.seed}")
        print(f"multiplier(a) = {self.multiplier}")
        print(f"increment(c) = {self.increment}")
        print(f"modulus(M) = {self.modulus}")

    def get_seed(self):
        return self.seed

    def set_seed(self, new_seed):
        """
        We use this function to reset our random seed
        :param new_seed:
        :return:
        """
        self.seed = new_seed
        return None

    def initial_gen(self):
        self.seed = 1

    def recurrence(self):
        """
        This is the LCG calculation formula
        :return:
        """
        return np.mod((self.multiplier * self.seed + self.increment), self.modulus)

    def next_random(self):
        """
        fomular is
        X1 = (a * X0 + c) mod M
        :return:
        """
        self.seed = self.recurrence()
        return self.seed

    def seq_random(self, length):
        """
        :param length: the length of this random number list
        :return: a list of random number
        """
        seq_list = []
        self.seed = 1
        for i in range(length):
            seq = self.seed / self.modulus
            self.seed = self.recurrence()
            seq_list.append(seq)
        return seq_list



class SCG(LCG):
    """
    inherited from LCG
    Xn+1 = (Xn(Xn + 1)) mod M
    The seed of this generator has to satisfy X0 mod 4 = 2
    """

    def __init__(self):
        self.seed = np.int64(6)
        self.multiplier = np.int64(1103515245)
        self.increment = np.int64(12345)
        # modulus(M) represent the int32 max limitation, so we need use int64 to initial Mb
        self.modulus = np.power(2, 32, dtype=np.int64)
        print(f"Our initial parameters: seed(X0) = {self.seed}")
        print(f"multiplier(a) = {self.multiplier}")
        print(f"increment(c) = {self.increment}")
        print(f"modulus(M) = {self.modulus}")

    def set_seed(self, new_seed):
        if np.mod(new_seed, 4) == 2:
            self.seed = new_seed
            print(f"You have successfully set seed as {self.seed}")
        else:
            print(f"Please input a seed mod with 4 is 2.")

    def recurrence(self):
        return np.mod((self.seed * (self.seed + 1)), self.modulus)

test_1 = LCG()
seq_list = test_1.seq_random(10)
print(seq_list)
test_2 = SCG()
seq_list = test_2.seq_random(10)
print(seq_list)

