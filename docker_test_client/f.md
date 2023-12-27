# Structure
- ### Manager node : 1, Workers node : 3   
    Workers Status: Active or Drain(Unactive)

    Horizontal scaling up or down by **[CPU usage]**   
    - CPU usage is 80% of limit on every worker node in 3 seconds. --> Horizontal scaling up one worker node (Status: **Drain(Unactive) -> Active**).
    - CPU usage is 20% of limit on every worker node in 3 seconds. --> Horizontal scaling down one worker node (Status: **Active -> Drain(Unactive)**)

    Manager node is agent server that updating a routing table and worker nodes are backend servers.

    Agent server handles requests by Python **Async structure**

- ### Load Balance Policy
    Agent server receives request and scans routing table to choose **Least usage of CPU in worker nodes** and transmits the request to the server which was chosen.


- ### Test Client : 1   
    Send requests with a cycle **[0, 1, 2, 1]** and interval is **0.01** second by multiprocess pool. Full cycle time is 0.04 seconds and sum of requests is 4000.   

    - **Request Data**   
        number: Calculating the sum of prime numbers from 0 to requested number.
    - **Response Data**
        number: --
        count: Sum of prime numbers
        CPU usage list : Response from agent routing table for every worker node.
        run time: calculated time on backend server without transmited and responsed time.

# Model
- ### Data set
    4000 records.
    The 4000 data is divided into training set, validation set and testing set.
- ### LSTM
    Time step is 10.   
    **Model Sequetial**   
    - LSTM layer: working units are 100, activation function is **Relu**
    - Full connected layer : unit is 1 **(Output)**

    **Fit**
    - epochs is 200, batch size is 32
    Use early_stopping function preventing overfitting.
    


- Add memory data   
- Add predicting model to agent server
- Load balance policy