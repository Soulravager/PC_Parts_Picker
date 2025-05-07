'''
@login_required
def profile_view(request):
    # Fetch builds for the logged-in user
    builds = Build.objects.filter(user=request.user)

    print(f'Builds for {request.user.username}: {builds}')  # Log the builds to check

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'parts/profile.html', {
        'form': form,
        'builds': builds,
    })'''
'''


@login_required
def pc_buildr(request):
    if request.method == 'POST':
        build_name = request.POST.get('build_name')
        cpu_id = request.POST.get('cpu')
        motherboard_id = request.POST.get('motherboard')
        gpu_id = request.POST.get('gpu')
        ram_id = request.POST.get('ram')
        ssd_id = request.POST.get('ssd')
        psu_id = request.POST.get('psu')

        # Make sure all components are selected
        if not all([cpu_id, motherboard_id, gpu_id, ram_id, ssd_id, psu_id]):
            print("One or more components were not selected.")
            return render(request, 'parts/pc_builder.html', {
                'cpus': CPU.objects.all(),
                'motherboards': Motherboard.objects.all(),
                'gpu': GPU.objects.all(),
                'rams': RAM.objects.all(),
                'ssds': SSD.objects.all(),
                'psu': PSU.objects.all(),
                'error': 'Please select all components.'
            })
        
        # Retrieve components and create the build
        cpu = CPU.objects.get(id=cpu_id)
        motherboard = Motherboard.objects.get(id=motherboard_id)
        gpu = GPU.objects.get(id=gpu_id)
        ram = RAM.objects.get(id=ram_id)
        ssd = SSD.objects.get(id=ssd_id)
        psu = PSU.objects.get(id=psu_id)

        # Create the build and link it to the current user
        Build = Build.objects.create(
            name=build_name,
            user=request.user,
            cpu=cpu,
            motherboard=motherboard,
            gpu=gpu,
            ram=ram,
            ssd=ssd,
            psu=psu
        )

        return redirect('parts/profile.html')  # Redirect to the profile page after saving the build
    
    # Render the PC builder form
    cpus = CPU.objects.all()
    motherboards = Motherboard.objects.all()
    gpus = GPU.objects.all()
    
    # Fetch RAM and provide a default if no entries exist
    rams = RAM.objects.all()
    if not rams:
        # Adding a default RAM entry for testing or fallback
        rams = [RAM(name="Default RAM", id=1)]  # You can customize this entry
    
    ssds = SSD.objects.all()
    psu = PSU.objects.all()

    return render(request, 'parts/pc_builder.html', {
        'cpus': cpus,
        'motherboards': motherboards,
        'gpus': gpus,
        'rams': rams,  # Pass the default (or empty) RAM entries
        'ssd': ssds,
        'psu': psu,
    })




from django.http import JsonResponse
from django.shortcuts import render
from .models import CPU, Motherboard, GPU, RAM, SSD, PSU

def component_detailszz(request, component_type):
    # Fetch details based on component type (CPU, Motherboard, etc.)
    if component_type == 'cpu':
        components = CPU.objects.all()
    elif component_type == 'motherboard':
        components = Motherboard.objects.all()
    elif component_type == 'gpu':
        components = GPU.objects.all()
    elif component_type == 'ram':
        components = RAM.objects.all()
    elif component_type == 'ssd':
        components = SSD.objects.all()
    elif component_type == 'psu':
        components = PSU.objects.all()
    else:
        components = []

    # Prepare the data as a list of dictionaries
    component_data = []
    for component in components:
        component_data.append({
            'name': component.name,
            'details': component.details  # Assuming 'details' is a field in your models
        })

    return JsonResponse(component_data, safe=False)


def profile_view(request):
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after saving
    else:
        form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'parts/profile.html', {'form': form})'''


'''def pc_builder(request):
    # Retrieve all components and print them for debugging
    users = User.objects.all()
    cpu = CPU.objects.all()
    motherboards = Motherboard.objects.all()
    gpus = GPU.objects.all()
   # rams = RAM.objects.all()
    #ssds = SSD.objects.all()
    #psus = PSU.objects.all()

    # print("CPUs:", cpu)  # Debugging statement
    # print("Motherboards:", motherboards)
    # print("GPUs:", gpus)
    # print("RAMs:", rams)
    # print("SSDs:", ssds)
    # print("PSUs:", psus)

    # Pass data to template context
    context = {
        'users': users,
        'cpu': cpu,
        'motherboards': motherboards,
        'gpus': gpus
        # 'rams': rams,
        # 'ssds': ssds,
        # 'psus': psus,
    }

    return render(request, 'pc_builder.html', context)'''

'''def pc_builder(request):
    # Fetch all components from the database
    cpus = CPU.objects.all()
    gpus = GPU.objects.all()
    motherboards = Motherboard.objects.all()
    rams = RAM.objects.all()
    ssds = SSD.objects.all()
    psus = PSU.objects.all()

    # Pass the components to the template
    return render(request, 'parts/pc_builder.html', {
        'cpus': cpus,
        'gpus': gpus,
        'motherboards': motherboards,
        'rams': rams,
        'ssds': ssds,
        'psus': psus,
    })
'''

