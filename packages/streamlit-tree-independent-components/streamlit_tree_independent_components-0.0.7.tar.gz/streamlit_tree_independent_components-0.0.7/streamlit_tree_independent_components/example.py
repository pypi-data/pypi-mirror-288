import streamlit as st
from my_component import my_component

# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run my_component/example.py`

st.subheader("Component with input args")

# Create an instance of our component with a constant `name` arg, and
# print its output value.
treeItems =  {
  "id": "0",
  "name": "Parent",
  "icon":"folder",
  'disable':False,
  "children": [
    {
      "id": "1",
      "name": "Child - 1",
      "icon":"folder",
    },
    {
      "id": "2",
      "name": "Child - 2",
      "icon":"document",
      'disable':False,
      "children": [
        {
          "id": "3",
          "name": "Child - 3",
          "icon":"document",
          "children": [
            {
              "id": "4",
              "name": "Child - 4",
              "icon":"settings",
            },
            {
              "id": "5",
              "name": "Child - 5",
              "icon":"folder",
              "children": [
                {
                  "id": "6",
                  "name": "Child - 6",
                  "icon":"settings",
                  "disable":False
                },
              ],
            },
          ],
        },
      ],
    },
    {
      "id": "7",
      "name": "Child - 7",
      "icon":"folder",
      'disable': True,
      "children": [
        {
          "id": "8",
          "name": "Child - 8",
          "icon":"folder",
          'disable': False
        },
      ],
    },
  ],
}
checkItems = ["0","1","2","3","4","5","6","7"]

result = my_component(treeItems, checkItems, expandItems=checkItems)

st.write(result)

# Create a second instance of our component whose `name` arg will vary
# based on a text_input widget.
#
# We use the special "key" argument to assign a fixed identity to this
# component instance. By default, when a component's arguments change,
# it is considered a new instance and will be re-mounted on the frontend
# and lose its current state. In this case, we want to vary the component's
# "name" argument without having it get recreated.
#name_input = st.text_input("Enter a name", value="Streamlit")
#num_clicks = my_component(name_input, key="foo")
#st.markdown("You've clicked %s times!" % int(num_clicks))
