# Test Mode

We need to automate the evaluation and statistics of ai.

> How to do this? Players will encounter wild pokemon on the turf.

## Start test

You can use `--fight-test` to entrance fight test mode. All user operation will be blocked. I suggest you use `--shell` to easy change the game state.

And there are some other augrements.

1. `--test-count <number>`
   The total test count.
2. `--test-settings <setting name>`
   Look the `./test/data`, there have many things about memory recoved settings.
   Before the every fight, the memory will be changed.
   The format of the file is yaml type file. It is `<memory addr>:<data>`. We aready write some settings in this floder, you can used.

> [!TIP]
> The test velocity abosbsy for API speed and animation.
>
> API speed is difficut to contral. But we can use `--skip-animation` to skip the `0.01s` sleep for each tick.

## End test

The test is be saved for each fight. If you use `Ctrl-C` to stop, the data will not be lost.

It will be saved in `./test_record`.
