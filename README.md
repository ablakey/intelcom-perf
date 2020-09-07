# Intelcom Performance Analysis

A mostly pointless project to see if I can understand delivery times based on the emails they send me.

Whenever I have an Intelcom-based delivery, I get an email when it's "on it's way!" and then when delivered. If I go through the history of these emails, I can learn how long it typically is for delivery once the first email is received.

The emails also include a line like this: "Drivername is currently completing delivery number 76, you are delivery number 114." From this I might be able to tell how long these intermediate deliveries take, which might give me a more accurate estimate of delivery times.

## Mbox format

Readable in plaintext. I know absolutely nothing about this format at the moment. But amazingly (maybe not) Python has a built-in `mailbox` library that handles it.

I want to iterate through every email, and regex a few strings.



## Email Layout

I want some elements of each email. From a skim, the emails seem similar enough. Here are the facts as I know them:

- Each delivery has 2 emails: "On the way!" and "Delivered"
- Each will have a datetime from the email header
- Email A will have the driver name (bonus)c
- Email A will have your delivery index number and the current delivery index number the driver is on (eg.  44 of 74)

## Plan

### Data Structure
- delivery_id: string
- start_date: Date
- end_date: Date
- current_delivery_number: int
- my_delivery_number: int

### Script
There's not a lot of emails so I'm not implementing any concurrency yet.

1. For each file in `emails/`
2. Parse with `mailbox` in some way
3. Get datetime from header
4. Regex elements from body and title
5. Populate structure for each
6. Do some analysis, print some output, maybe show a chart

### Analysis
This part I kind of suck at. I'm sure the stats experts know how to do this.
- look at how many minutes it takes to deliver once the first email is sent
- how many minutes per delivery this is (ie. if I'm 74 and they're on 44, how many mins each of those 30 deliveries takes)
- calculate the average delivery time once first email is sent
- plot the distribution somehow? Understand how reliable this average is

## Validation

- Populate every field. If any field is unpopulated, throw an error and we'll investigate and understand better (probably regex error)
