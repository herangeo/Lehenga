import os
import google.generativeai as genai

genai.configure(api_key="AIzaSyBF2PqA8tGr-yQ09DlRolNZ9KzQA7GJUbs")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash-exp",
  generation_config=generation_config,
)

def GenerateResponse(input_text):

    response = model.generate_content([
    "input: What lehengas do you have in pink?",
    "output: We have a variety of pink lehengas! Some popular options are Floral Pink Embroidered Lehenga and Pastel Pink Georgette Lehenga. Would you like to see more details or pictures?",
    "input: Show me lehengas with heavy embroidery.",
    "output: Sure! We have heavily embroidered lehengas in different styles. Some options are Velvet Bridal Lehenga and Designer Zari Work Lehenga. Can I help you choose one?",
    "input: What is the price range for lehengas?",
    "output: Our lehengas range from ₹5,000 to ₹50,000. Do you have a specific budget in mind?",
    "input: Do you have any discounts or offers?",
    "output: Yes! Currently, we are offering up to 20% off on select lehengas. Would you like to explore discounted options?",
    "input: Can I customize the color of the lehenga?",
    "output: Yes, we offer color customization on many lehengas. Let me know which design you like, and we’ll guide you through the options",
    "input: What sizes are available for lehengas?",
    "output: Our lehengas are available in sizes S, M, L, XL, and custom measurements. Would you like assistance with sizing?",
    "input: How long does delivery take?",
    "output: Delivery usually takes 7–10 business days. For customized lehengas, it may take an additional 5 days. Would you like to proceed with an order?",
    "input: What is your return policy?",
    "output: We accept returns within 7 days of delivery for non-customized products in their original condition. Let us know if you need help with a return!",
    "input: Can I talk to a customer care representative?",
    "output: Certainly! Please provide your email or phone number, and our representative will contact you shortly.",
    "input: Do you have matching accessories?",
    "output: No we sell only lehengas here",
    f"input: {input_text}",
    "output: ",
    ])

    return response.text


while True:
    string = str(input("Enter your prompt:"))
    print("Bot:",GenerateResponse(string))