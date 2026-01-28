# Smart Nutrition System - Activity Diagram (Scan & Log Food)

```mermaid
activityDiagram-v2
    start
    :User navigates to "Scan & Log" page;
    
    if (Select Mode) then (Image Scan)
        :User uploads Image;
        :User clicks "Scan Label";
        :System sends image to OCR Service;
        if (OCR Success?) then (Yes)
            :System extracts text;
            :LLM parses nutrition info;
            :Return nutrition JSON;
        else (No)
            :Show Error Message;
            stop
        endif
    else (Barcode Scan)
        :User scans Barcode;
        :System queries OpenFoodFacts API;
        if (Product Found?) then (Yes)
            :Return nutrition JSON;
        else (No)
            :Show "Product Not Found" Error;
            stop
        endif
    endif

    :Display "Nutrition Extracted" Form;
    :User reviews Food Name & Macros;
    :User inputs "Quantity Consumed";
    
    if (User clicks "Save & Log") then (Yes)
        :System creates new Food Item (DB);
        :System logs Meal Entry (DB);
        :Update User Streak;
        :Redirect to Dashboard;
        stop
    else (Cancel)
        :Clear Data;
        :Return to Scan Mode;
        stop
    endif
```
