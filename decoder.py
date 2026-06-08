from django.shortcuts import redirect, render

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.session.get('User')

        if not user:
            return redirect('mainapp:Login')

        if user.get('Role') != 'Admin':
            return render(request, 'error.html', {
                'error': 'You are not allowed to access Admin Panel'
            })

        return view_func(request, *args, **kwargs)

    return wrapper


def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.session.get('User')

        if not user:
            return redirect('mainapp:Login')

        if user.get('Role') != 'Staff':
            return render(request, 'error.html', {
                'error': 'You are not allowed to access Staff Panel'
            })

        return view_func(request, *args, **kwargs)

    return wrapper


def login_required_custom(view_func):
    def wrapper(request, *args, **kwargs):
        user = request.session.get('User')

        if not user:
            return redirect('mainapp:Login')

        return view_func(request, *args, **kwargs)

    return wrapper