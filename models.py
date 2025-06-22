class ProfileMatchingModel:
    CRITERIA = {
        'ipk': {'weight': 0.25, 'target': 4},
        'jaringan_komputer': {'weight': 0.20, 'target': 4},
        'bahasa_pemrograman': {'weight': 0.20, 'target': 5},
        'komunikasi_tim': {'weight': 0.20, 'target': 4},
        'disiplin_tanggungjawab': {'weight': 0.15, 'target': 4}
    }
    
    IPK_SCALE = [
        {'range': (3.80, 4.00), 'value': 5},
        {'range': (3.20, 3.79), 'value': 4},
        {'range': (2.80, 3.19), 'value': 3},
        {'range': (2.00, 2.79), 'value': 2},
        {'range': (0.00, 1.99), 'value': 1}
    ]
    
    GAP_VALUES = {
        0: 6,
        1: 5.5,
        -1: 5,
        2: 4.5,
        -2: 4,
        3: 3.5,
        -3: 3,
        4: 2.5,
        -4: 2,
        5: 1.5,
        -5: 1
    }
    
    @classmethod
    def calculate_ipk_value(cls, ipk):
        for scale in cls.IPK_SCALE:
            if scale['range'][0] <= ipk <= scale['range'][1]:
                return scale['value']
        return 0
    
    @classmethod
    def calculate_gap(cls, actual, target):
        return actual - target
    
    @classmethod
    def calculate_core_factor(cls, gap_value):
        return cls.GAP_VALUES.get(gap_value, 0)
    
    @classmethod
    def calculate_final_score(cls, candidate_data):
        ipk_value = cls.calculate_ipk_value(candidate_data['ipk'])
        gaps = {
            'ipk': cls.calculate_gap(ipk_value, cls.CRITERIA['ipk']['target']),
            'jaringan_komputer': cls.calculate_gap(candidate_data['jaringan_komputer'], cls.CRITERIA['jaringan_komputer']['target']),
            'bahasa_pemrograman': cls.calculate_gap(candidate_data['bahasa_pemrograman'], cls.CRITERIA['bahasa_pemrograman']['target']),
            'komunikasi_tim': cls.calculate_gap(candidate_data['komunikasi_tim'], cls.CRITERIA['komunikasi_tim']['target']),
            'disiplin_tanggungjawab': cls.calculate_gap(candidate_data['disiplin_tanggungjawab'], cls.CRITERIA['disiplin_tanggungjawab']['target'])
        }
        
        core_factors = {k: cls.calculate_core_factor(v) for k, v in gaps.items()}
        
        final_score = sum(
            core_factors[k] * cls.CRITERIA[k]['weight'] 
            for k in cls.CRITERIA.keys()
        )
        
        return final_score
    
    @classmethod
    def rank_candidates(cls, candidates):
        scored_candidates = []
        for candidate in candidates:
            data = {
                'id': candidate[0],
                'name': candidate[1],
                'ipk': candidate[2],
                'jaringan_komputer': candidate[3],
                'bahasa_pemrograman': candidate[4],
                'komunikasi_tim': candidate[5],
                'disiplin_tanggungjawab': candidate[6]
            }
            
            final_score = cls.calculate_final_score(data)
            scored_candidates.append({
                **data,
                'final_score': final_score
            })
        
        ranked_candidates = sorted(
            scored_candidates, 
            key=lambda x: x['final_score'], 
            reverse=True
        )
        
        for i, candidate in enumerate(ranked_candidates, 1):
            candidate['ranking'] = i
        
        return ranked_candidates