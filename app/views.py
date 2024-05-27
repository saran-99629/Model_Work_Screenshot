from django.shortcuts import render
import pickle
import os
from django.conf import settings
# Create your views here.
def index(request):
    return render(request,'index.html')
    
def urlprocess(request):
    screenshots = capture_screenshots_with_browser(interval=10, duration=60)
    res_fin = []
    url_input=''
    if request.method == 'POST':
        url_input = request.POST.get('url_input', '')
        filename = 'C:/Users/tmachine/Desktop/work/django_model/app/model_naive_bayes.sav'
        try:
            with open(filename, 'rb') as model_file:
                model = pickle.load(model_file)
            result = model.predict([url_input])
            res_fin.append(result[0])
        except FileNotFoundError:
            return render(request, 'result.html', {'error': 'Model file not found.'})
    
    return render(request, 'result.html', {'res_fin': res_fin, 'screenshots':screenshots})



from django.shortcuts import render
from django.http import HttpResponse
import pyautogui
import time
import subprocess

def is_browser_window_open():
    browser_processes = ['chrome.exe', 'firefox.exe', 'msedge.exe','brave.exe']
    process = subprocess.Popen(['tasklist'], stdout=subprocess.PIPE)
    output, _ = process.communicate()
    for browser_process in browser_processes:
        if browser_process.encode() in output:
            return True
    return False
import os 



def capture_screenshots_with_browser(interval=10, duration=60):
    end_time = time.time() + duration
    screenshots = []
    screenshot_count = 1
    while time.time() < end_time:
        if is_browser_window_open():
            screenshot = pyautogui.screenshot()
            screenshot_path = f'C:/Users/tmachine/Desktop/work/django_model/app/static/screenshots/screenshot_{screenshot_count}.png'
            screenshot.save(screenshot_path)
            screenshots.append(screenshot_path)
            screenshot_count += 1
        time.sleep(interval)
    
    return screenshots


import psutil
from collections import defaultdict


def get_running_apps():
    apps = defaultdict(lambda:{'count':0,'cpu_time':0})
    total_processes = 0 
    total_cpu_time=0
    for proc in psutil.process_iter(['pid', 'name','cpu_times']):
        try:
            username = proc.username()
        except psutil.AccessDenied:
            username = 'AccessDenied'
        
        if username !='SYSTEM':
            apps[proc.info['name']]['count']+=1
            apps[proc.info['name']]['cpu_time'] += sum(proc.info['cpu_times'])
            total_processes+=1 
            total_cpu_time+=sum(proc.info['cpu_times'])
        return apps,total_processes, total_cpu_time

def calculate_percentage(apps, total_cpu_time):
    for app in apps:
        apps[app]['percentage'] = (apps[app]['cpu_time'] / total_cpu_time) * 100 if total_cpu_time > 0 else 0
    return apps


def running_app_view(request):
    running_apps, total_processes, total_cpu_time = get_running_apps()
    running_apps = calculate_percentage(running_apps, total_cpu_time)
    
    apps_data = []
    for app, details in running_apps.items():
        apps_data.append({
            'name': app, 
            'count': details['count'], 
            'cpu_time': details['cpu_time'], 
            'percentage': details['percentage']
        })
    
    context = {'apps_data': apps_data}
    return render(request, 'process.html', context)