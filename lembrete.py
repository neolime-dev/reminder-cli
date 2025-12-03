#!/usr/bin/env python3
import sys
import re
import time
import subprocess
import datetime

def print_usage():
    print("""Uso: lembrete "Mensagem" <tempo>

Exemplos:
  lembrete "Tirar o lixo" 10m
  lembrete "Reunião" 1h
  lembrete "Daily" 15:30""")

def parse_time(time_str):
    # Tenta relativo (10m, 1h)
    match_rel = re.match(r'^(\d+)([hms])$', time_str)
    if match_rel:
        val = int(match_rel.group(1))
        unit = match_rel.group(2)
        if unit == 's': return val
        if unit == 'm': return val * 60
        if unit == 'h': return val * 3600
    
    # Tenta absoluto (15:30)
    match_abs = re.match(r'^(\d{1,2}):(\d{2})$', time_str)
    if match_abs:
        now = datetime.datetime.now()
        h = int(match_abs.group(1))
        m = int(match_abs.group(2))
        target = now.replace(hour=h, minute=m, second=0, microsecond=0)
        
        if target < now:
            # Se já passou, avisa
            return -1
        
        delta = target - now
        return int(delta.total_seconds())

    return None

def main():
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    msg = sys.argv[1]
    time_str = sys.argv[2]
    
    seconds = parse_time(time_str)
    
    if seconds is None:
        print(f"Erro: Formato de tempo '{time_str}' inválido.")
        print_usage()
        sys.exit(1)
        
    if seconds < 0:
        print(f"Erro: O horário {time_str} já passou hoje.")
        sys.exit(1)
    
    # Escapar aspas simples para o shell
    safe_msg = msg.replace("'", "'\\''")
    
    # Comando para rodar em background independente
    # sleep X && notify-send ...
    cmd = f"sleep {seconds} && notify-send -a 'Lembrete' 'Lembrete' '{safe_msg}' -u critical"
    
    # Executa desconectado
    subprocess.Popen(['sh', '-c', cmd], start_new_session=True)
    
    # Calcula horario final para feedback visual
    finish_time = (datetime.datetime.now() + datetime.timedelta(seconds=seconds)).strftime('%H:%M:%S')
    
    print(f"✅ Lembrete agendado!")
    print(f"Msg: {msg}")
    print(f"Toca às: {finish_time}")

if __name__ == "__main__":
    main()
