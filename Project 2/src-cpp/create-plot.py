import matplotlib.pyplot as plt

class Test:
    def __init__(self, size, jacobi, gauss_seidel, lu):
        self.size = size
        self.jacobi = jacobi
        self.gauss_seidel = gauss_seidel
        self.lu = lu
    
    def __str__(self):
        return f"{self.size} {self.jacobi} {self.gauss_seidel} {self.lu}"

data = []
with open("raw-output.txt", "r") as f:
    N = None
    counter = 0
    for line in f:
        line = line.strip().replace("\0", "")
        if line == "": 
            continue
        if N is not None:
            if counter == 0:
                jacobi = float(line)
            elif counter == 1:
                gauss_seidel = float(line)
            elif counter == 2:
                lu = float(line)
                data.append(Test(N, jacobi, gauss_seidel, lu))
                N = None
            counter = (counter + 1) % 3
        if line.startswith("N"):
            N = int(line[3:])

for test in data:
    print(test)

test_sizes = [test.size for test in data]
plots_dir = '../plots'

plt.figure(figsize=(10, 5))
plt.grid()
plt.plot(test_sizes, [result.jacobi for result in data], '-o', label='Metoda Jacobiego')
plt.plot(test_sizes, [result.gauss_seidel for result in data], '-o', label='Metoda Gaussa-Seidela')
plt.plot(test_sizes, [result.lu for result in data], '-o', label='Metoda LU')
plt.title('Czas wykonania metod zainplementowanych niskopoziomowo')
plt.xlabel('Rozmiar macierzy')
plt.ylabel('Czas [s]')
plt.legend()
plt.savefig(f'{plots_dir}/time-cpp.png', bbox_inches='tight')
plt.show()
        
