# Booking

### How should be done:

Users see a list of all available seats. Usually each user is given some time to check the seat details, seat view etc.
So when a user is on a seat page, frontend sends a request letting backend now that a user is interest. Backend will
then lock the seat for a short period of time, and maybe letting other clients know (in case we're using a websocket to
track changes), and no one else will be able to book or check the seat unless the time we allowed user is passed (and
maybe we got a request from frontend letting us know that user is no longer interested).

Same we do the same when a user is requested a payment link to pay for the seat if available. We probably allow longer
time for payments. Then we'll verify the payment and finalize the booking for user.

Note that we should be careful with our queries since data might change while we're processing another request. We're
using SQL which provides us with ACID capability so a transaction will help us to avoid such a problem and roll back in
case anything changed while we're processing the request.

### Current implementation:

Current implementation is just a simple way of showing the steps needed to implement the full system. It requires way
more validation and APIs.