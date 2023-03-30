import dimod
import numpy as np
import streamlit as st

# Definimos la función que resolverá el problema de la mochila con el simulador clásico
def solve_knapsack(items, weights, values, max_weight):
    # Creamos el modelo de la mochila
    model = dimod.BinaryQuadraticModel.from_numpy_matrix(items, offset=0.0)
    
    # Agregamos las restricciones de peso
    for i in range(len(weights)):
        if weights[i] > max_weight:
            model.add_constraint({i: 1}, strength=weights[i] - max_weight)
            
    # Resolvemos el problema utilizando el simulador clásico
    sampler = dimod.ExactSolver()
    response = sampler.sample(model)
    
    # Decodificamos la respuesta y encontramos la mejor solución
    best_energy = np.inf
    best_solution = None
    
    for sample, energy in response.data(['sample', 'energy']):
        if energy < best_energy:
            best_energy = energy
            best_solution = sample
            
    # Calculamos el valor total de la solución encontrada
    total_value = sum(values[i] for i in best_solution)
    
    return best_solution, total_value

# Definimos la aplicación Streamlit
def main():
    st.title("Problema de la mochila con simulador clásico")
    
    # Definimos los inputs de la aplicación
    num_items = st.number_input("Número de elementos:", value=10)
    max_weight = st.number_input("Peso máximo:", value=50)
    
    items = np.random.randint(0, 2, size=(num_items, num_items))
    weights = np.random.randint(1, 10, size=num_items)
    values = np.random.randint(1, 10, size=num_items)
    
    # Resolvemos el problema y mostramos la solución
    if st.button("Resolver"):
        solution, total_value = solve_knapsack(items, weights, values, max_weight)
        
        st.write("Solución encontrada:")
        st.write(solution)
        st.write("Valor total de la solución:")
        st.write(total_value)

if __name__ == "__main__":
    main()
