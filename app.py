# --- ETAPA 3: MINERAÇÃO ---
def minerar_pool():
    pool = []
    L_MIN_BRUTA = LU_NOMINAL * L_MIN_FATOR 
    def varredura(idx, qtd, l_acum, vetor):
        if idx == len(larguras):
            if l_acum >= L_MIN_BRUTA and l_acum <= LU_MAX: pool.append({'vetor': list(vetor), 'l_real': l_acum})
            return
        max_q = min(MAX_FACAS - qtd, int((LU_MAX - l_acum) // larguras_efetivas[idx]))
        for q in range(max_q + 1):
            vetor[idx] = q
            varredura(idx + 1, qtd + q, l_acum + q * larguras_efetivas[idx], vetor)
            vetor[idx] = 0
    varredura(0, 0, 0.0, [0]*len(larguras))
    
    final_pool = []
    for p in pool:
        usadas = [larguras[i] for i in range(len(larguras)) if p['vetor'][i] > 0]
        if 0 < len(usadas) <= MAX_LARG_ESQUEMA:
            if len(usadas) > 1 and any(round(abs(w1 - w2), 1) < DIFF_LIMIT for w1, w2 in itertools.combinations(usadas, 2)): continue
            p['slu'] = ((LU_NOMINAL - p['l_real'])/LU_NOMINAL)*100
            p['tipo'] = "Mono" if len(usadas) == 1 else "Duo" if len(usadas) == 2 else "Trio"
            final_pool.append(p)
    return final_pool

pool_detalhado = minerar_pool()

# --- ETAPA 4: SOLVER ---
solver = pywraplp.Solver.CreateSolver('SCIP')
x = [solver.IntVar(0, 10000, f'x_{j}') for j in range(len(pool_detalhado))]
y = [solver.IntVar(0, 1, f'y_{j}') for j in range(len(pool_detalhado))]
underfill = [solver.IntVar(0, 100000, f'under_{i}') for i in range(len(larguras))]

for i in range(len(larguras)):
    prod = sum(pool_detalhado[j]['vetor'][i] * x[j] for j in range(len(pool_detalhado)))
    solver.Add(prod + underfill[i] >= demandas_rolos[i]) 
    solver.Add(prod <= math.ceil(demandas_rolos[i] * OTIF_MAX)) 
    solver.Add(underfill[i] <= math.ceil(demandas_rolos[i] * FOLGA)) 

for j in range(len(pool_detalhado)):
    solver.Add(x[j] <= 10000 * y[j])
    solver.Add(x[j] >= y[j] * MIN_RUNS_SETUP)

solver.Add(sum(y) <= MAX_SETUPS)

total_prod_kg_runs = sum(x[j] * ((pool_detalhado[j]['l_real'] * METRAGEM * G) / 1e6) for j in range(len(pool_detalhado)))
peso_dem_rolos = sum(demandas_rolos[i] * ((larguras[i] * METRAGEM * G) / 1e6) for i in range(len(larguras)))
excesso_kg = total_prod_kg_runs - peso_dem_rolos

custos_final = []
for j in range(len(pool_detalhado)):
    perda = LU_NOMINAL - pool_detalhado[j]['l_real']
    custos_final.append((perda * PREMIO_AVANCO) if perda < 0 else (perda * 10))

peso_falta_kg = sum(underfill[i] * ((larguras[i] * METRAGEM * G) / 1e6) for i in range(len(larguras)))

solver.Minimize(sum(x[j] * custos_final[j] for j in range(len(pool_detalhado))) + sum(x) * L1_TIRADAS + sum(y) * L2_SETUPS + excesso_kg * L3_OVER + peso_falta_kg * CUSTO_FALTA)
status = solver.Solve()
