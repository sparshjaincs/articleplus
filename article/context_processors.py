
from .models import Articles,Profile,activity,Notifications
def data(request):
    show =  False
    percentage = 0.0
    val = Articles.objects.filter(status = 'published').order_by('-date_Publish','-time')[:2]
    if request.user.is_authenticated:
        data1 = Profile.objects.filter(user=request.user).values_list('first_name','last_name','email','bio','phone_number','address','city','state','country','date_of_birth')
        profile_ins =  Profile.objects.get(user=request.user)
        count =0
        for value in data1[0]:
        
            if value == "---":
               count+=1
        if count>0:
            show = True
        else:
            show =  False
        length = len(data1[0])
        
        
        percentage =round((1-(count/length))*100)
        if percentage <=25:
            percentage=25
        chat=[]
        for i in Profile.objects.get(user=request.user).follow.all():
            if request.user in i.profile.follow.all():
                chat.append(i.profile)

        
        activ = activity.objects.filter(user_name3=request.user).order_by('-date_activity','-activity_time')
        if Notifications.objects.filter(user_name4 = request.user).exists():
            notify = Notifications.objects.get(user_name4 = request.user)
            activity_c= notify.activity_count
          
            original_act_count = activ.count()
           
            notify.activity_count = original_act_count
            notify.save()
            d_a_c = original_act_count - activity_c
            act_status = (False,) if d_a_c <= 0 else (True,d_a_c)
            
        else:
            act_status = (False,)

        
        

            
        
        


       
    else:
        profile_pic = ""
        chat=[]
        activ=[]
        act_status = (False,)
        
       


    
    return {'title1':val,"show":show,"percentage":percentage,"chat":chat,"activity":activ,'a_c':act_status}
