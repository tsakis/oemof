class Entity:
  """
  """
  def __init__(self, inputs = [], outputs = [], **kwargs):
    """
    :param uid: unique component identifier
    :param inputs: list of Entities acting as input to this Entity.
    :param outputs: list of Entities acting as output from this Enity.
    """
    self.uid = kwargs["uid"]
    self.inputs = inputs
    self.outputs = outputs
    for e_in in self.inputs:
      if self not in e_in.outputs: e_in.outputs.append(self)
    for e_out in self.outputs:
      if self not in e_out.inputs: e_out.inputs.append(self)

  def __str__(self): return "<{0} #{1}>".format(type(self).__name__, self.uid)

class Component(Entity): pass

class Transformer(Component):
 """
 """
 def __init__(self, **kwargs):
  """
  """
  super().__init__(**kwargs)
  if not self.inputs:
    raise ArgumentError("Transformer must have at least one input.\n" +
                        "Got: {0!r}".format(inputs))
  if not self.outputs:
    raise ArgumentError("Transformer must have at least one output.\n" +
                        "Got: {0!r}".format(outputs))

class Sink(Component):
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    if self.outputs:
      raise ArgumentError("Sink must not have outputs.\n" +
                          "Got: {0!r}".format(outputs))


class Source(Component):
  """
  """
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    if self.inputs:
      raise ArgumentError("Sink must not have inputs.\n" +
                          "Got: {0!r}".format(inputs))

class Bus(Entity):
  """
  """
  def __init__(self, **kwargs):
    """
    :param type: bus type could be electricity...BLARBLAR
    """
    super().__init__(**kwargs)
    self.type = kwargs["type"]

class Transport(Component):
  def __init__(self, **kwargs):
    """
    """
    super().__init__(**kwargs)
    if len(self.inputs) != 1:
      raise ArgumentError("Transport must have exactly one input.\n" +
                          "Got: {0!r}".format(inputs))

    if len(self.outputs) != 1:
      raise ArgumentError("Transport must have exactly one output.\n" +
                          "Got: {0!r}".format(outputs))




if __name__ == "__main__":
  #TODO: This example is missing a Transport. (Needs more escalation error.)
  coal = Bus(uid="Coal", type="coal")
  power = Bus(uid="Electricity", type="electricity")
  heat = Bus(uid="Thermal", type="thermal")
  heatpump = Transformer(uid="Heatpump", inputs=[power],
                         outputs=[heat])
  chp = Transformer(uid="CHP", inputs=[coal], outputs=[heat, power])
  wind = Source(uid="The only wind turbine on the planet.", outputs=[power])
  city = Sink(uid="Neverwhere", inputs=[heat])
