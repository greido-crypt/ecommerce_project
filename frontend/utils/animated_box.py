import asyncio

import flet as ft


class FormDataAnimatedBox:
    def __init__(self,
                 clock_wize_rotate: float):
        self.clock_wize_rotate = clock_wize_rotate


class AnimatedBox(FormDataAnimatedBox, ft.Container):
    def __init__(self, clock_wize_rotate: float, **kwargs):
        FormDataAnimatedBox.__init__(self, clock_wize_rotate)
        ft.Container.__init__(self, **kwargs)

        self.counter = 0

    def did_mount(self):
        self.page.run_task(self.startAnimatedBox)

    async def startAnimatedBox(self):

        while True:
            if self.counter < 5:
                self.rotate.angle -= self.clock_wize_rotate

                try:
                    await self.update_async()
                except AssertionError:
                    return

                self.counter += 1

                await asyncio.sleep(1)

            elif self.counter <= 10:
                self.counter += 1
                self.rotate.angle += self.clock_wize_rotate

                try:
                    await self.update_async()
                except AssertionError:
                    return

                await asyncio.sleep(1)

            elif self.counter > 10:
                self.counter = 0
                await asyncio.sleep(2)
