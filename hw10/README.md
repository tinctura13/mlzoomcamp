# Question 1
Here <value> is the probability of getting a credit card. You need to choose the right one.  
`0.7269`

# Question 2
What's the version of `kind` that you have?  
`kind version 0.20.0`

# Question 3
What's `CLUSTER-IP` of the service that is already running there?  
```
NAME         TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE
kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   11m
```

# Question 4
To be able to use the docker image we previously created (`zoomcamp-model:hw10`), we need to register it with `kind`.  
What's the command we need to run for that?  
`kind load docker-image`

# Question 5
What is the value for `Port`?  
`9696`  

Apply this deployment using the appropriate command and get a list of running Pods.  
You can see one running Pod.  
```
NAME                      READY   STATUS    RESTARTS   AGE
credit-65ccb78b69-s8ngt   1/1     Running   0          64s
```

# Question 6
Fill it in. What do we need to write instead of <???>?  
`credit`  

# Question 7
I don't know why but I didn't saw any changes here `:c`  
CPU load was the same all the time  
```
NAME         REFERENCE           TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
credit-hpa   Deployment/credit   <unknown>/20%   1         3         1          6m49s
```
