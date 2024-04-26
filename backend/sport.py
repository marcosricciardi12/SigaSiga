def select_sport(sport):
    
    marcador = {
        "basquet": {"equipo_local": "default",
                    "puntos_local": 0,
                    "faltas_local": 0,
                    "equipo_vista": "default",
                    "puntos_visita": 0,
                    "faltas_visita": 0,
                    "reloj_24": 0,
                    "tiempo": 0,
                    },
        "futbol": {},
        "voley": {},
    }

    estadisticas = {
        "basquet": {"equipo_local": "default",
                    "puntos_local": 0,
                    "faltas_local": 0,
                    "equipo_vista": "default",
                    "puntos_visita": 0,
                    "faltas_visita": 0,
        },
        "futbol": {},
        "voley": {},
    }

    return marcador[sport], estadisticas[sport]

sb, st = select_sport(input("seleccione deporte: "))
print(sb)
print(st)