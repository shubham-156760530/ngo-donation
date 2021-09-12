from django.shortcuts import render
from .forms import NgoDonationForm
from .models import NgoDonation
import razorpay

def ngo_donation(request):
    if request.method == 'POST':
        name = request.POST['name']
        amount = eval(request.POST['amount'])*100

        #create razorpay client
        client = razorpay.Client(auth=('rzp_test_Ki1Kw2Z1hhvly7', 'AEg5FHNsrSKOMyKEvsoHOk9L'))

        #create order
        response_payment = client.order.create(dict( amount = amount, currency = 'INR' ))
        #print(response_payment)
        order_id = response_payment['id']
        order_status = response_payment['status']
        
        if order_status == 'created':
            ngo_donation = NgoDonation( name = name, amount = amount, order_id = order_id)
            ngo_donation.save()        
            response_payment['name'] = name
            form = NgoDonationForm(request.POST or None)
            return render(request, 'ngo_payment.html', {'form':form, 'payment':response_payment})

    form = NgoDonationForm()
    return render(request, 'ngo_payment.html', {'form':form})



def payment_status(request):
    response = request.POST
    #print(response)
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']
    }

    # client instance
    client = razorpay.Client(auth=('rzp_test_Ki1Kw2Z1hhvly7', 'AEg5FHNsrSKOMyKEvsoHOk9L'))

    try:
        status = client.utility.verify_payment_signature(params_dict)
        ngo_donation = NgoDonation.objects.get(order_id = response['razorpay_order_id'])
        ngo_donation.razorpay_payment_id = response['razorpay_payment_id']
        ngo_donation.paid = True
        ngo_donation.save()
        return render(request, 'payment_status.html', {'status':True})
    except:
        return render(request, 'payment_status.html', {'status':False})

# Create your views here.
