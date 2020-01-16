## possible issues?

- functions/modules are tight coupled

    very high risk to brake code by implicit change

- props drilling

    ```
    env:namespaces                                          < --- env config
    env:code

    -> lambda_handler(event, context)                       < --- entry point / front controller
        -> build_result(context, key, namespaces, code)     < --- modules
            -> request_status(context, namespace, code)
                -> _sanitize_code(code)
    ```

- tests are not adequate

    it's hard to mock/stub dependencies of `count_items()`

    questions:

    - are these tests isolated? `NO`
    - is source code loosely coupled? `NO`
    - are these tests maintainable? `NO`
    - do they really perform unittest? `NO`

    notes:

    - requires to mock whole hierarchy
    - there are some hidden non-easy testable resources (boto3 seesion/client)
