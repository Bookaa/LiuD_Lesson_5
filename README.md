# LiuD_Lesson_5
LiuD lesson five

In lesson 4,

        g_prefix
        g_skipspace

these 2 global variable is not good. Lets define it in GDL

    option.prefix = LiuD
    states.skip = space
    main = (stmt1 NEWLINE)*
    stmt1 = options | stmt
    options = option1 | state1
        option1 = 'option.prefix' '=' NAME
        state1 = 'states.skip' '=' NAME
    stmt = NAME '=' stmt_value
    stmt_value = values_or | string_or | jiap | series
        values_or = NAME ^+ '|'
        string_or = STRING ^+ '|'
        series = value*
        jiap = NAME '^+' STRING

    litname = NAME
    litstring = STRING
    value1 = litname | litstring | enclosed
        enclosed = '(' stmt_value ')'
    value = itemd | value1
        itemd = value1 '*'
