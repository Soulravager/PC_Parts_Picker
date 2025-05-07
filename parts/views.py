from django.shortcuts import render
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileUpdateForm
from .models import CPU, GPU, Motherboard
from .models import Build 
from django.shortcuts import get_object_or_404

@login_required
def your_main_view(request):
    # Your view logic here
    return render(request, 'parts/main_page.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'parts/signup.html', {'form': form})

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Build, Purchase, Favorite,Cart,Part_sale
from .forms import ProfileUpdateForm

@login_required
def profile_view(request):
    user = request.user

    # Ensure the user has a profile
    profile, created = Profile.objects.get_or_create(user=user)

    # Fetch builds, purchases, and favorite items
    builds = Build.objects.filter(user=user)
    purchases = Purchase.objects.filter(user=user)
    favorite_items = Favorite.objects.filter(user=user, is_favorite=True).exclude(part_model__isnull=True)
    cart_items = Cart.objects.filter(user=user, is_cart=True).exclude(part_model__isnull=True)
    part_sale = Purchase.objects.filter(user=user)
    part_purchases = Part_sale.objects.filter(user=user).order_by('-purchased_at')

    # Calculate total price for each build
    builds_with_total = []
    for build in builds:
        total_price = (
            (build.cpu.price if build.cpu else 0) +
            (build.motherboard.price if build.motherboard else 0) +
            (build.gpu.price if build.gpu else 0) +
            (build.ram.price if build.ram else 0) +
            (build.ssd.price if build.ssd else 0) +
            (build.psu.price if build.psu else 0)
        )
        builds_with_total.append({'build': build, 'total_price': total_price})

    # Handle profile form submission
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile)
    
    return render(request, 'parts/profile.html', {
        'form': form,
        'builds_with_total': builds_with_total,
        'purchases': purchases,
        'favorite_items': favorite_items,
        'cart_items': cart_items,
        'part_sale':part_sale,
        'part_purchases': part_purchases 

    })

@login_required
def delete_buildd(request, build_id):
    # Get the build by ID and ensure it belongs to the logged-in user
    build = get_object_or_404(Build, id=build_id, user=request.user)
    
    if request.method == 'POST':
        build.delete()
        #messages.success(request, 'Build removed successfully.')
        return redirect('profile')
    
    return render(request, 'parts/delete_confirmation.html', {'build': build})

@login_required
def delete_build(request, build_id):
    build = get_object_or_404(Build, id=build_id, user=request.user)  # Check that the build belongs to the user
    if request.method == 'POST':
        build.delete()
       # messages.success(request, 'Build deleted successfully.')
        return redirect('profile')
    else:
       # messages.error(request, 'Invalid request method.')
        return redirect('profile')

@login_required
def toggle_share_build(request, build_id):
    build = get_object_or_404(Build, id=build_id, user=request.user)

    # Toggle the 'shareable' status
    build.shareable = not build.shareable
    build.save()

    return redirect('profile')  # Redirect back to profile page
from django.shortcuts import render
from .models import CPU, GPU, Motherboard#, RAM, SSD, PSU
from django.contrib.auth.models import User


#def index(request):
 #   return render(request, 'parts/index.html')

def index(request):
    return render(request, 'parts/index.html')

def about_us(request):
    return render(request, 'parts/about-us.html')

def build_help(request):
    return render(request, 'parts/build-help.html')

def contacts(request):
    return render(request, 'parts/contact.html')

def typography(request):
    return render(request, 'parts/typography.html')

def pc_builder(request):
    return render(request, 'parts/pc_builder.html')

from django.shortcuts import render

def error(request, exception=None):  # Accept exception argument
    return render(request, 'parts/error.html', status=404)

 
 ##PC BUILD NEW
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CPU, GPU, Motherboard, RAM, SSD, PSU, Build
@login_required
def pc_build(request):
    cpus = CPU.objects.all()
    gpus = GPU.objects.all()
    ssds = SSD.objects.all()
    psus = PSU.objects.all()
    motherboards = Motherboard.objects.all()
    rams = RAM.objects.all()

    if request.method == 'POST':
        build_name = request.POST.get('build_name')
        cpu_model = request.POST.get('cpu')
        motherboard_model = request.POST.get('motherboard')
        gpu_model = request.POST.get('gpu')
        ram_model = request.POST.get('ram')
        ssd_model = request.POST.get('ssd')
        psu_model = request.POST.get('psu')

        # Retrieve components
        cpu = CPU.objects.get(id=cpu_model)
        motherboard = Motherboard.objects.get(id=motherboard_model)
        ram = RAM.objects.get(id=ram_model)
        gpu = GPU.objects.get(id=gpu_model)
        ssd = SSD.objects.get(id=ssd_model)
        psu = PSU.objects.get(id=psu_model)

        # Backend validation: CPU and Motherboard compatibility
        if cpu.CPU_socket != motherboard.socket_type:
            return render(request, 'parts/pc_builder.html', {
                'cpus': cpus,
                'motherboards': motherboards,
                'gpus': gpus,
                'rams': rams,
                'ssds': ssds,
                'psus': psus,
                'error': 'The selected motherboard is not compatible with the CPU.'
            })

        # Backend validation: RAM and Motherboard compatibility
        if ram.type != motherboard.RAM_Type:
            return render(request, 'parts/pc_builder.html', {
                'cpus': cpus,
                'motherboards': motherboards,
                'gpus': gpus,
                'rams': rams,
                'ssds': ssds,
                'psus': psus,
                'error': 'The selected RAM is not compatible with the motherboard.'
            })

        # Create the build
        Build.objects.create(
            name=build_name,
            user=request.user,
            cpu=cpu,
            motherboard=motherboard,
            gpu=gpu,
            ram=ram,
            ssd=ssd,
            psu=psu
        )

        return redirect('profile')

    return render(request, 'parts/pc_builder.html', {
        'cpus': cpus,
        'motherboards': motherboards,
        'gpus': gpus,
        'rams': rams,
        'ssds': ssds,
        'psus': psus,
    })

from django.http import JsonResponse
from .models import Motherboard, RAM, CPU

def get_motherboards(request):
    socket = request.GET.get('socket')  # Fetch the CPU socket type from the request
    motherboards = Motherboard.objects.filter(socket_type=socket).values('id', 'name', 'model', 'RAM_Type', 'socket_type', 'image_url', 'description', 'price')
    return JsonResponse(list(motherboards), safe=False)

def get_ram(request):
    ram_type = request.GET.get('type')  # Fetch RAM type from the request
    rams = RAM.objects.filter(type=ram_type).values('id', 'name', 'model', 'image_url', 'description', 'price')
    return JsonResponse(list(rams), safe=False)


#Component Details 
#BEFORE P_)PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
from django.http import JsonResponse
from parts.models import CPU, Motherboard

def component_details(request, component_type):
    if component_type == 'cpu':
        components = CPU.objects.all()
    elif component_type == 'motherboard':
        components = Motherboard.objects.all()
    # Add additional logic for other components (GPU, RAM, etc.)

    # Prepare data to send as JSON response
    data = []
    for component in components:
        data.append({
            'name': component.name,
            'details': component.details,  # Assuming you have a 'details' field
        })
    
    return JsonResponse(data, safe=False)

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import CPU, GPU, Motherboard, RAM, SSD, PSU, Build
from .models import Purchase

@login_required
def purchase_view   (request):
    if request.method == 'POST':
        # Gather the selected component IDs from the form
        cpu_id = request.POST.get('cpu')
        motherboard_id = request.POST.get('motherboard')
        gpu_id = request.POST.get('gpu')
        ram_id = request.POST.get('ram')
        ssd_id = request.POST.get('ssd')
        psu_id = request.POST.get('psu')

        # Retrieve the selected components from the database
        cpu = CPU.objects.get(id=cpu_id)
        motherboard = Motherboard.objects.get(id=motherboard_id)
        gpu = GPU.objects.get(id=gpu_id)
        ram = RAM.objects.get(id=ram_id)
        ssd = SSD.objects.get(id=ssd_id)
        psu = PSU.objects.get(id=psu_id)

        # Calculate the total price
        total_price = (
            cpu.price +
            motherboard.price +
            gpu.price +
            ram.price +
            ssd.price +
            psu.price
        )

        # Create a new purchase record
        purchase = Purchase.objects.create(
            user=request.user,
            build_name=request.POST.get('build_name'),
            cpu=cpu,
            motherboard=motherboard,
            gpu=gpu,
            ram=ram,
            ssd=ssd,
            psu=psu,
            total_price=total_price
        )

        # Redirect to a confirmation or summary page (optional)
        return render(request, 'parts/purchase_summary.html', {
            'cpu': cpu,
            'motherboard': motherboard,
            'gpu': gpu,
            'ram': ram,
            'ssd': ssd,
            'psu': psu,
            'total_price': total_price,
        })

    return render(request, 'parts/purchase.html', {
        'cpus': CPU.objects.all(),
        'motherboards': Motherboard.objects.all(),
        'gpus': GPU.objects.all(),
        'rams': RAM.objects.all(),
        'ssds': SSD.objects.all(),
        'psus': PSU.objects.all(),
    })

def confirm_purchase_view(request):
    if request.method == 'POST':
        # Handle the purchase confirmation logic here
        return render(request, 'parts/purchase_confirmation.html')
    return render(request, 'parts/purchase_summary.html')
    


#CHAT BOT GEMINI 
from django.shortcuts import render
from django.http import JsonResponse
import google.generativeai as genai

genai.configure(api_key="AIzaSyBS6zUQANjgspTU1DT4C1PHdfJrmDngOA4")
# Define generation configuration (as per your app.py)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize the model with the generation configuration
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction=(
        "Only answer computer-related topics. This chat is for a PC builder chatbot.\n"
        "If the user asks something unrelated, either ask for clarification or reply with:\n"
        "'I can only answer that Related to PC Building.'\n"
        "Focus on PC-building or computer hardware/software issues."
    ),
)

def generate_response(prompt):
    """Generates a response from the Gemini API based on the given prompt."""
    try:
        # Start a new chat session with the system instruction
        chat_session = model.start_chat(
            history=[{
                "role": "user",
                "parts": [
                    "Only answer computer-related topics. This chat is for a PC builder chatbot.\n"
                    "If the user asks something unrelated, either ask for clarification or reply with:\n"
                    "'I can only answer that in PC Builder.'\n"
                    "Focus on PC-building or computer hardware/software issues.\n"
                    "Make the text short so that its clear to read \n"
                    "words inside ** should be bold and dont use ** ** in the chat okay this can be achieved by simple explanations "
                ],
            }]
        )

        # Send the user's prompt and generate a response
        response = chat_session.send_message(prompt)

        # Return the generated response text
        return response.text.strip() if response.text else "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"An error occurred: {e}"

def chatbot_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input')
        ai_response = generate_response(user_input)
        return JsonResponse({'user_input': user_input, 'ai_response': ai_response})
    
    return render(request, 'chatbot.html')

##SHARE BUILD
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from .models import Build

def shared_build_detail(request, build_id):
    # Get the build object
    build = get_object_or_404(Build, id=build_id)

    # Check if the build is shareable; if not, return a 404 error
    if not build.shareable:
        #raise Http404("This build is not shared.")
        return redirect('error')

    # Calculate total price (assuming each part has a 'price' field)
    total_price = (
        build.cpu.price + build.gpu.price + build.motherboard.price +
        build.ram.price + build.ssd.price + build.psu.price
    )

    return render(
        request,
        "shared_build.html",
        {"build": build, "total_price": total_price}
    )
from django.shortcuts import render
from .models import Build

def shared_builds_list(request):
    shared_builds = Build.objects.filter(shareable=True)  # Fetch only shared builds
    return render(request, "shared_builds_list.html", {"shared_builds": shared_builds})


##SHARE BUILD
def part_detail(request, part_model):
    # Identify the correct part and its category
    if CPU.objects.filter(model=part_model).exists():
        part = CPU.objects.get(model=part_model)
        category = "cpu"
    elif GPU.objects.filter(model=part_model).exists():
        part = GPU.objects.get(model=part_model)
        category = "gpu"
    elif Motherboard.objects.filter(model=part_model).exists():
        part = Motherboard.objects.get(model=part_model)
        category = "motherboard"
    elif RAM.objects.filter(model=part_model).exists():
        part = RAM.objects.get(model=part_model)
        category = "ram"
    elif SSD.objects.filter(model=part_model).exists():
        part = SSD.objects.get(model=part_model)
        category = "ssd"
    elif PSU.objects.filter(model=part_model).exists():
        part = PSU.objects.get(model=part_model)
        category = "psu"
    else:
        return render(request, '404.html', status=404)  # Handle not found

    # Get reviews and ratings
    reviews = Review.objects.filter(part_model=part.model)
    avg_rating = UserRating.objects.filter(part_model=part.model).aggregate(Avg('rating'))['rating__avg'] or 0

    return render(request, 'parts/part_detail.html', {
        'part': part,
        'category': category,  # Pass category to template
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'form': ReviewForm(),
        'rating_form': RatingForm(),
    })
#FOR BUILD COMPONENT PARTS
def component_list(request, part_model):
    # Identify the correct part and its category
    if CPU.objects.filter(model=part_model).exists():
        part = CPU.objects.get(model=part_model)
        category = "cpu"
    elif GPU.objects.filter(model=part_model).exists():
        part = GPU.objects.get(model=part_model)
        category = "gpu"
    elif Motherboard.objects.filter(model=part_model).exists():
        part = Motherboard.objects.get(model=part_model)
        category = "motherboard"
    elif RAM.objects.filter(model=part_model).exists():
        part = RAM.objects.get(model=part_model)
        category = "ram"
    elif SSD.objects.filter(model=part_model).exists():
        part = SSD.objects.get(model=part_model)
        category = "ssd"
    elif PSU.objects.filter(model=part_model).exists():
        part = PSU.objects.get(model=part_model)
        category = "psu"
    else:
        return render(request, '404.html', status=404)  # Handle not found

    # Get reviews and ratings
    reviews = Review.objects.filter(part_model=part.model)
    avg_rating = UserRating.objects.filter(part_model=part.model).aggregate(Avg('rating'))['rating__avg'] or 0

    return render(request, 'parts/component_4build.html', {
        'part': part,
        'category': category,  # Pass category to template
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'form': ReviewForm(),
        'rating_form': RatingForm(),
    })

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Avg
from .models import CPU, GPU, Motherboard, RAM, SSD, PSU, UserRating, Review

def part_details(request, part_id, category):
    # Identify the correct part and its category
    category = category.lower()  # Normalize category to lowercase
    part = None

    if category == "cpu":
        part = get_object_or_404(CPU, id=part_id)
    elif category == "gpu":
        part = get_object_or_404(GPU, id=part_id)
    elif category == "motherboard":
        part = get_object_or_404(Motherboard, id=part_id)
    elif category == "ram":
        part = get_object_or_404(RAM, id=part_id)
    elif category == "ssd":
        part = get_object_or_404(SSD, id=part_id)
    elif category == "psu":
        part = get_object_or_404(PSU, id=part_id)
    else:
        return JsonResponse({'error': 'Invalid category'}, status=400)

    # Fetch ratings & reviews
    reviews = Review.objects.filter(part_model=part.model)
    avg_rating = UserRating.objects.filter(part_model=part.model).aggregate(Avg('rating'))['rating__avg'] or 0

    return render(
        request,
        'parts/part_detail_ajax.html',
        {
            'part': part,
            'avg_rating': round(avg_rating, 1),
            'reviews': reviews,
            'selected_category': category  # Pass category to template
        }
    )




##asf

##

from django.shortcuts import render
from django.db.models import Avg  #  Correctly import Avg
from .models import CPU, GPU, Motherboard, RAM, SSD, PSU, Review, Favorite, UserRating,Cart
from .forms import ReviewForm, RatingForm
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Avg

def parts_list(request):
    category = request.GET.get('category', 'cpu')

    # Fetch parts based on category
    model_map = {
        'cpu': CPU,
        'gpu': GPU,
        'motherboard': Motherboard,
        'ram': RAM,
        'ssd': SSD,
        'psu': PSU,
    }
    parts = model_map.get(category, CPU).objects.all()

    # Calculate average rating
    for part in parts:
        ratings = UserRating.objects.filter(part_model=part.model)
        part.avg_rating = round(ratings.aggregate(Avg('rating'))['rating__avg'] or 0, 1)

    # Fetch user's favorite parts
    favorite_items = (
        Favorite.objects.filter(user=request.user, is_favorite=True).values_list('part_model', flat=True)
        if request.user.is_authenticated
        else []
    )
    
    cart_items = (
        Cart.objects.filter(user=request.user, is_cart=True).values_list('part_model', flat=True)
        if request.user.is_authenticated
        else []
    )
    # Handle AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  
        html = render_to_string('parts/parts_list_ajax.html', {'parts': parts, 'favorite_items': favorite_items, 'cart_items': cart_items}, request=request)
        return JsonResponse({'html': html})

    return render(request, 'parts/parts_list.html', {'category': category, 'parts': parts, 'favorite_items': favorite_items, 'cart_items': cart_items})

#RATING TO MODELS>RATING PARTS
from django.http import JsonResponse
from django.db.models import Avg
from .models import CPU, GPU, Motherboard, RAM, SSD, PSU, UserRating

def update_part_ratings(request):
    """Update the rating field for all parts (CPU, GPU, etc.) based on user ratings."""
    
    model_mapping = {
        "cpu": CPU,
        "gpu": GPU,
        "motherboard": Motherboard,
        "ram": RAM,
        "ssd": SSD,
        "psu": PSU,
    }

    updated_parts = []

    for category, model_class in model_mapping.items():
        # Get all parts for this category
        parts = model_class.objects.all()

        # Get all ratings for these parts
        part_models = [part.model for part in parts]
        ratings_data = UserRating.objects.filter(part_model__in=part_models).values("part_model").annotate(avg_rating=Avg("rating"))

        # Convert ratings to dictionary
        ratings_dict = {r["part_model"]: round(r["avg_rating"] or 1) for r in ratings_data}

        # Update each part's rating field
        for part in parts:
            new_rating = ratings_dict.get(part.model, 1)  # Default to 1 if no ratings
            if part.rating != new_rating:  # Only update if changed
                part.rating = new_rating
                part.save(update_fields=["rating"])
                updated_parts.append(f"{category.upper()} - {part.model}")

    return JsonResponse({"status": "success", "updated_parts": updated_parts})

from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def submit_review(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            part_model = request.POST.get("part_model")  # Get part model
            category = request.POST.get("category")  # Get category

            # Check if user already reviewed this part and category
            existing_review = Review.objects.filter(user=request.user, part_model=part_model, category=category).first()

            if existing_review:
                # Update existing review
                existing_review.content = form.cleaned_data["content"]
                existing_review.save()

                return JsonResponse({
                    "success": True,
                    "message": "Review updated!",
                    "user": existing_review.user.username,
                    "content": existing_review.content,
                    "date": existing_review.created_at.strftime("%Y-%m-%d %H:%M")
                })

            else:
                # Create a new review
                review = form.save(commit=False)
                review.user = request.user
                review.part_model = part_model
                review.category = category
                review.save()

                return JsonResponse({
                    "success": True,
                    "message": "Review submitted!",
                    "user": review.user.username,
                    "content": review.content,
                    "date": review.created_at.strftime("%Y-%m-%d %H:%M")
                })
    
    return JsonResponse({"success": False, "error": "Invalid form submission"}, status=400)


##rating
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .forms import RatingForm
from django.http import JsonResponse
from .models import UserRating


@login_required
def submit_rating(request):
    if request.method == "POST":
        form = RatingForm(request.POST)
        part_model = request.POST.get("part_model")

        if form.is_valid():
            rating_value = form.cleaned_data["rating"]
            user = request.user

            user_rating, created = UserRating.objects.get_or_create(
                user=user, part_model=part_model, defaults={"rating": rating_value}
            )

            if not created:
                user_rating.rating = rating_value
                user_rating.save()

            # Calculate updated average rating
            avg_rating = UserRating.objects.filter(part_model=part_model).aggregate(Avg("rating"))["rating__avg"]

            return JsonResponse({"success": True, "avg_rating": round(avg_rating, 1)})

    return JsonResponse({"success": False, "error": "Invalid data"}, status=400)


###Favorite 
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Favorite, CPU, GPU, Motherboard, RAM, SSD, PSU

@login_required
def toggle_favorite(request, part_model):
    part = (
        CPU.objects.filter(model=part_model).first() or
        GPU.objects.filter(model=part_model).first() or
        Motherboard.objects.filter(model=part_model).first() or
        RAM.objects.filter(model=part_model).first() or
        SSD.objects.filter(model=part_model).first() or
        PSU.objects.filter(model=part_model).first()
    )
    if not part:
            return redirect('parts_list')
    favorite, created = Favorite.objects.get_or_create(user=request.user, part_model=part_model)
    favorite.part_name = part.name
    favorite.is_favorite = not favorite.is_favorite
    favorite.save()
    return redirect('parts_list')

@login_required
def favorite_profile(request, part_model):
    favorite = Favorite.objects.filter(user=request.user, part_model=part_model).first()

    if favorite:
        print(f"Removing {favorite.part_name} from favorites")  # Debug log
        favorite.delete()

    return redirect('profile')



#staff


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import CPU, GPU, RAM, SSD, Motherboard, PSU
from .forms import CPUForm, GPUForm, RAMForm, SSDForm, MotherboardForm, PSUForm

# Mapping categories to models & forms
model_form_map = {
    'cpu': (CPU, CPUForm),
    'gpu': (GPU, GPUForm),
    'ram': (RAM, RAMForm),
    'ssd': (SSD, SSDForm),
    'motherboard': (Motherboard, MotherboardForm),
    'psu': (PSU, PSUForm),
}

#  Staff Dashboard (Loads categories & parts)
@login_required
def staff_dashboard(request, category="cpu"):
    if not request.user.is_staff:
        return redirect('error')

    model, _ = model_form_map.get(category, (None, None))
    if not model:
        return redirect('staff_dashboard', category="cpu")

    parts = model.objects.all()
    return render(request, 'staff_dashboard.html', {
        'categories': model_form_map.keys(),
        'parts': parts,
        'category': category
    })

#  Add a new part
@login_required
def staff_add_part(request, category):
    if not request.user.is_staff:
        return redirect('home')

    model, form_class = model_form_map.get(category, (None, None))
    if not model:
        return redirect('staff_dashboard')

    if request.method == "POST":
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('staff_dashboard', category=category)
    else:
        form = form_class()

    return render(request, 'staff_dashboard.html', {
        'categories': model_form_map.keys(),
        'form': form,
        'category': category,
        'parts': model.objects.all()
    })

#  Edit an existing part
@login_required
def staff_edit_part(request, category, part_id):
    if not request.user.is_staff:
        return redirect('home')

    model, form_class = model_form_map.get(category, (None, None))
    if not model:
        return redirect('staff_dashboard')

    part = get_object_or_404(model, id=part_id)

    if request.method == "POST":
        form = form_class(request.POST, request.FILES, instance=part)
        if form.is_valid():
            form.save()
            return redirect('staff_dashboard', category=category)
    else:
        form = form_class(instance=part)

    return render(request, 'staff_dashboard.html', {
        'categories': model_form_map.keys(),
        'form': form,
        'category': category,
        'parts': model.objects.all(),
        'editing': True,
        'part': part
    })

#  Delete a part
@login_required
def staff_delete_part(request, category, part_id):
    if not request.user.is_staff:
        return redirect('home')

    model, _ = model_form_map.get(category, (None, None))
    if not model:
        return redirect('staff_dashboard')

    part = get_object_or_404(model, id=part_id)
    part.delete()
    return redirect('staff_dashboard', category=category)

#CHAT TELEGRAM
import requests
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Replace with your bot token and admin chat ID
TELEGRAM_BOT_TOKEN = "7725781198:AAHaGtm5eh9j-xN1cl1xBFiRKXZ4O72qSUM"
TELEGRAM_CHAT_ID = "754112013"

def send_telegram_message(name, email, phone, message):
    """Sends message to the admin via Telegram"""
    text = f"📩 *New Enquiry Submission*\n\n" \
           f"👤 *Name:* {name}\n" \
           f"✉️ *Email:* {email}\n" \
           f"📞 *Phone:* {phone}\n" \
           f"💬 *Message:* {message}"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}

    response = requests.post(url, json=payload)
    return response.status_code == 200

@csrf_exempt  # Disable CSRF for simplicity; ensure you handle security properly
def contact_form_submission(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        if name and email and message:
            success = send_telegram_message(name, email, phone, message)
            if success:
                return JsonResponse({"status": "success", "message": "Message sent successfully!"})
            else:
                return JsonResponse({"status": "error", "message": "Failed to send message."})
        return JsonResponse({"status": "error", "message": "Missing required fields."})
    
    return JsonResponse({"status": "error", "message": "Invalid request method."})
#Newsletter

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Replace with your actual bot token and chat ID
TELEGRAM_BOT_TOKEN = "7725781198:AAHaGtm5eh9j-xN1cl1xBFiRKXZ4O72qSUM"
TELEGRAM_CHAT_ID = "754112013"

def send_newsletter_notification(email):
    """Sends a newsletter subscription notification to the admin via Telegram."""
    text = f"📢 *New Newsletter Subscription*\n\n" \
           f"✉️ *Email:* {email}"

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": text, "parse_mode": "Markdown"}

    response = requests.post(url, json=payload)
    return response.status_code == 200

@csrf_exempt
def newsletter_subscription(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if email:
            success = send_newsletter_notification(email)
            if success:
                return JsonResponse({"status": "success", "message": "Subscription successful!"})
            else:
                return JsonResponse({"status": "error", "message": "Failed to send notification."})
        return JsonResponse({"status": "error", "message": "Email is required."})

    return JsonResponse({"status": "error", "message": "Invalid request method."})




##CHAT BOT COMMS 


import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import google.generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyBS6zUQANjgspTU1DT4C1PHdfJrmDngOA4")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Initialize Gemini Model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
    system_instruction=(
        "Only answer computer-related topics. This chat is for a PC builder chatbot.\n"
        "If the user asks something unrelated, either ask for clarification or reply with:\n"
        "'I can only answer that Related to PC Building.'\n"
        "Focus on PC-building or computer hardware/software issues."
    ),
)

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "7975838794:AAHfZiKrWdITrJSmuYJU1JLmoot-y4z-smE"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def telegram_generate_response(prompt):
    """Generate a response from the Gemini AI model."""
    try:
        chat_session = model.start_chat(
            history=[{"role": "user", "parts": ["Keep responses concise and PC-building focused."]}]
        )
        response = chat_session.send_message(prompt)
        return response.text.strip() if response.text else "Sorry, I couldn't generate a response."
    except Exception as e:
        return f"An error occurred: {e}"

def telegram_send_message(chat_id, message):
    """Send a message back to the user via Telegram."""
    payload = {"chat_id": chat_id, "text": message}
    requests.post(TELEGRAM_API_URL, json=payload)

@csrf_exempt
def telegram_webhook(request):
    """Handle incoming messages from Telegram bot."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Extract user ID and message
            chat_id = data["message"]["chat"]["id"]
            user_message = data["message"]["text"]

            # Generate Gemini response
            bot_response = telegram_generate_response(user_message)

            # Send response back to Telegram user
            telegram_send_message(chat_id, bot_response)

        except Exception as e:
            print(f"Error processing message: {e}")

    return JsonResponse({"status": "ok"})


###CART parts sales etc
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CPU, GPU, Motherboard, RAM, SSD, PSU


@login_required
def toggle_cart(request, part_model):
    part = (
        CPU.objects.filter(model=part_model).first() or
        GPU.objects.filter(model=part_model).first() or
        Motherboard.objects.filter(model=part_model).first() or
        RAM.objects.filter(model=part_model).first() or
        SSD.objects.filter(model=part_model).first() or
        PSU.objects.filter(model=part_model).first()
    )

    if not part:
        return redirect('parts_list')

    cart_item, created = Cart.objects.get_or_create(user=request.user, part_model=part_model)
    cart_item.part_name = part.name
    cart_item.is_cart = not cart_item.is_cart  # Toggle the value
    cart_item.save()

    return redirect('parts_list')

@login_required
def cart_profile(request, part_model):
    part = (
        CPU.objects.filter(model=part_model).first() or
        GPU.objects.filter(model=part_model).first() or
        Motherboard.objects.filter(model=part_model).first() or
        RAM.objects.filter(model=part_model).first() or
        SSD.objects.filter(model=part_model).first() or
        PSU.objects.filter(model=part_model).first()
    )

    if not part:
        return redirect('profile')

    cart_item, created = Cart.objects.get_or_create(user=request.user, part_model=part_model)
    cart_item.part_name = part.name
    cart_item.is_cart = not cart_item.is_cart  # Toggle the value
    cart_item.save()

    return redirect('profile')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, Part_sale, CPU, GPU, Motherboard, RAM, SSD, PSU,Profile


from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, Part_sale, Profile, CPU, GPU, Motherboard, RAM, SSD, PSU

@login_required
def purchase_parts(request):
    # Get user profile and check address
    user_profile = Profile.objects.filter(user=request.user).first()
    
    if not user_profile or not user_profile.address:
        messages.error(request, "⚠️ Please update your address in the profile page to continue.")
    
    
    cart_items = Cart.objects.filter(user=request.user, is_cart=True)

    if request.method == "POST":
        # Move items to Part_sale
        Part_sale.objects.bulk_create([
            Part_sale(user=request.user, part_model=item.part_model, part_name=item.part_name)
            for item in cart_items
        ])

        # Remove all cart items after purchase
        cart_items.delete()

        return redirect("profile")  # Redirect to profile after purchase

    # Fetch all parts data
    all_parts = {
        **{cpu.name: cpu for cpu in CPU.objects.all()},
        **{gpu.name: gpu for gpu in GPU.objects.all()},
        **{mobo.name: mobo for mobo in Motherboard.objects.all()},
        **{ram.name: ram for ram in RAM.objects.all()},
        **{ssd.name: ssd for ssd in SSD.objects.all()},
        **{psu.name: psu for psu in PSU.objects.all()},
    }

    # Enrich cart items with part details
    for item in cart_items:
        part = all_parts.get(item.part_name)
        item.brand = part.brand if part else "Unknown"
        item.price = part.price if part else "N/A"
        item.image = part.image.url if part and part.image else None  

    total_price = sum(item.price for item in cart_items if item.price != "N/A")

    return render(request, "parts_sale.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "user_address": user_profile.address,
    })


#####STAFF REPORT PAGE##
from django.shortcuts import render
from django.db.models import Sum
from django.http import HttpResponse
import csv
from .models import Profile, Build, Purchase, Part_sale, CPU, GPU, Motherboard, RAM, SSD, PSU

from django.shortcuts import render
from django.db.models import Sum
from django.http import HttpResponse
import csv
from .models import Profile, Build, Purchase, Part_sale, CPU, GPU, Motherboard, RAM, SSD, PSU

def get_part_price(part_model):
    """Fetch the price of a part by looking up its model number in each part table."""
    part_classes = [CPU, GPU, Motherboard, RAM, SSD, PSU]
    
    for part_class in part_classes:
        part = part_class.objects.filter(model=part_model).first()
        if part:
            return part.price  # Return the first matching price
    
    return 0  # Default to 0 if not found

def staff_report(request):
    if not request.user.is_staff:
        return redirect('error')
    # Summary Data
    total_users = Profile.objects.count()
    total_builds = Build.objects.count()
    total_build_purchases = Purchase.objects.count()
    total_build_revenue = Purchase.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
    total_part_sales = Part_sale.objects.count()

    # Calculate total part sale revenue
    part_sales_data = Part_sale.objects.all()
    total_part_sale_revenue = sum(get_part_price(sale.part_model) for sale in part_sales_data)

    total_purchases = total_build_purchases + total_part_sales
    total_revenue = total_build_revenue + total_part_sale_revenue

    # Default: Show All Data
    users_data = Profile.objects.select_related('user').all()
    builds_data = Build.objects.select_related('user').all()
    purchases_data = Purchase.objects.all()

    # Filtering Logic
    report_type = request.GET.get('report', 'all')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if start_date and end_date:
        if report_type in ['builds', 'all']:
            builds_data = builds_data.filter(created_at__range=[start_date, end_date])
        if report_type in ['purchases', 'all']:
            purchases_data = purchases_data.filter(purchase_date__range=[start_date, end_date])
        if report_type in ['part_sales', 'all']:
            part_sales_data = part_sales_data.filter(purchased_at__range=[start_date, end_date])

    # Add part prices to part sales data
    part_sales_data = [
        {
            'user': sale.user.username,
            'part_model': sale.part_model,
            'part_name': sale.part_name,
            'part_price': get_part_price(sale.part_model)
        }
        for sale in part_sales_data
    ]

    # Calculate totals for reports
    total_purchase_price = sum(purchase.total_price for purchase in purchases_data)
    total_part_sales_price = sum(sale["part_price"] for sale in part_sales_data)

    # Handle CSV Download
    if request.GET.get('download') == "1":
        return download_report(report_type, users_data, builds_data, purchases_data, part_sales_data, total_purchase_price, total_part_sales_price)

    return render(request, 'staff_report.html', {
        'total_users': total_users,
        'total_builds': total_builds,
        'total_build_purchases': total_build_purchases,
        'total_build_revenue': total_build_revenue,
        'total_part_sales': total_part_sales,
        'total_part_sale_revenue': total_part_sale_revenue,
        'total_purchases': total_purchases,
        'total_revenue': total_revenue,
        'users_data': users_data,
        'builds_data': builds_data,
        'purchases_data': purchases_data,
        'part_sales_data': part_sales_data,
        'total_purchase_price': total_purchase_price,
        'total_part_sales_price': total_part_sales_price,
        'report_type': report_type,
        'start_date': start_date,
        'end_date': end_date,
    })

def download_report(report_type, users_data, builds_data, purchases_data, part_sales_data, total_purchase_price, total_part_sales_price):
    """Generates a CSV report for the selected report type."""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{report_type}_report.csv"'
    
    writer = csv.writer(response)

    if report_type == "users":
        writer.writerow(["Username"])
        for user in users_data:
            writer.writerow([user.user.username])

    elif report_type == "builds":
        writer.writerow(["User", "Build Name"])
        for build in builds_data:
            writer.writerow([build.user.username, build.name])

    elif report_type == "purchases":
        writer.writerow(["ID", "Build Name", "Total Price"])
        for purchase in purchases_data:
            writer.writerow([purchase.id, purchase.build_name, purchase.total_price])
        writer.writerow([])
        writer.writerow(["Total Purchases Price", "", total_purchase_price])

    elif report_type == "part_sales":
        writer.writerow(["User", "Part Model", "Part Name", "Part Price"])
        for sale in part_sales_data:
            writer.writerow([sale["user"], sale["part_model"], sale["part_name"], sale["part_price"]])
        writer.writerow([])
        writer.writerow(["Total Part Sales Price", "", "", total_part_sales_price])

    return response
