CREATE CONTINUOUS QUERY cq_payment_count2 ON example BEGIN SELECT count(amount) INTO example.autogen.payment_count2 FROM example.autogen.payments GROUP BY time(1m) END
