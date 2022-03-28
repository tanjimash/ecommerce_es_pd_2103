from django.shortcuts import redirect


def stop_unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        # print(request.user.is_authenticated)
        if not request.user.is_authenticated:
            return redirect('userRegApp:signin')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


