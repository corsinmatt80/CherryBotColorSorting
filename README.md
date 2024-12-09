# LaundrySorter

The LaundrySorter can be used with a Cherrybot to sort a pile of laundry, into four baskets, light, dark, colored and unsortable, in the UI the user can select the baskets in which the bot will place the clothes, he also gets live updates on how full each basket is.

# Instructions

IMPORTANT:
- The Laundry Sorter only works with cherrybot2 because it needs the ceiling camera.
- The Laundry Sorter will automatically get the access token when it starts, so it should only be started when no one else is using the robot.
- There are 3 hardcoded image/robot coordinate pairs in /backend/utils/image_to_robot.py, if these are not set correctly, the robot will not move to the baskets correctly.
- We have noticed that the robot's z coordinates can change from one session to another, since they are hardcoded this can cause problems with the cloth pickup. If this happens, the z coordinate for the pickup can be changed in /backend/robot_control/sort_clothes.py on line 36.



To start the application execute in the /src directory

```bash
  python app.py
```

Access the applicaiton at

http://127.0.0.1:5000


## Basket Detection

IMPORTANT 
- There are hardcoded coordinates for the pickup area where the laundry should be placed for the robot to pick it up, NO BASKETS should be placed over that area.

- If you are unsure where the pickup is the base_image_cropped.jpg in the source directory can be checked, but its basically just right in front of the robot, centered on the wooden table.

If no baskets have been detected, the Start sorting button is disabled; in this case, the Detect baskets button must be pressed.

Loading the basket detection page may take several seconds.

To make it easier for the application to detect the baskets, white paper squares are recommended.

The interface will show all the baskets detected, from which four can be selected by clicking on them; once exactly four are selected, the Accept button can be pressed to return to the home page.

## Start Sorting

When the Start Sorting button is pressed, the Pickup Area should be empty because the application is capturing a reference image that will be used to detect if any clothes are placed.

Once the Start Sorting button is pressed, it takes about 10 seconds before sorting actually starts because the application needs to make sure that the robot is in its initial position before capturing the reference image.

It will be clear that the sorting has started when the counts for each bin are displayed in the UI and/or there are repeated NO CLOTHES DETECTED prints in the console.

At this point you can start placing clothes in the pickup area (small pieces recommended), since the z-value for the pickup is fixed, the pile of clothes shouldn't be too high.

The robot will continue sorting as long as it detects a cloth in the pickup area, or until one of the baskets is full (at 10 pieces).

The full basket is indicated to the user with a notification.

## Closing the application

There is no way to delete the token through our applicaiton, so it should be deleted via swaggerhub.
