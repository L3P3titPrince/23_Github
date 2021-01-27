from py_01_gentic import Test


def main():
    """
    """
    test_class = Test()
    test_class.noise_point()

    x, y, weight_arr, x_arr= test_class.genetic_algorithm

    return x, y

    """
    1) Please plot the noisy data and the polynomial you found (in the same figure). 
    You can use any value of m selected from 2, 3, 4, 5, 6.

    2) Plot MSE versus order m, for m = 1, 2, 3, 4, 5, 6, 7, 8 respectively. Identify the best choice of m.

    3) Change variable noise_scale to 150, 200, 400, 600, 1000 respectively, re-run the algorithm 
    and plot the polynomials with the m found in 2). Discuss the impact of noise scale to the accuracy of the returned parameters. 
    [You need to plot a figure like in 1) for each choice of noise_scale.]

    4) Change variable number_of_samples to 40, 30, 20, 10 respectively, 
    re-ran the algorithm and plot the polynomials with the m found in 2). 
    Discuss the impact of the number of samples to the accuracy of the returned parameters. 
    [You need to plot a figure like in 1) for each choice of number_of_samples.]
    """

if __name__=="__main__":
    x, y, weight_arr, x_arr = main()