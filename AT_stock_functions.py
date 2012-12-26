


class Functions():
    def bind_stock(self,s):
        self.s = s


    def calculate_list_EMA(self,list):

        EMA_multiplier = self.s.EMA_1_multiplier
        EMA_list = []

        for item in list:
            if len(list) < 5:
                EMA = item
            else:
                new_EMA = ((item - list[-1]) * EMA_multiplier + list[-1])
                EMA = new_EMA
            EMA_list.append(EMA)

        return EMA_list

    def calculate_variable_EMA(self,v,list_of_list):

        EMA_multiplier_list = [self.s.EMA_1_multiplier,self.s.EMA_2_multiplier,self.s.EMA_3_multiplier]
        EMA_list = []
        counter = 0

        for list in list_of_list:
            if len(list) < 5:
                EMA = v
            else:
                new_EMA = ((v - list[-1]) * EMA_multiplier_list[counter]) + list[-1]
                EMA = new_EMA
                counter += 1
            EMA_list.append(EMA)

        return EMA_list

    def EMA(self):
        price_EMA = self.calculate_variable_EMA(self.s.price,(self.s.EMA_1_list,self.s.EMA_2_list,self.s.EMA_3_list))
        self.s.EMA_1 = price_EMA[0]
        if self.s.time_num % 2 == 0 or self.s.EMA_2 is None:
            self.s.EMA_2 = price_EMA[1]
        if self.s.time_num % 3 == 0 or self.s.EMA_3 is None:
            self.s.EMA_3 = price_EMA[2]
        self.s.EMA_1_list.append(self.s.EMA_1)
        self.s.EMA_2_list.append(self.s.EMA_2)
        self.s.EMA_3_list.append(self.s.EMA_3)

#        volume_EMA = self.calculate_variable_EMA(self.volume,(self.volume_EMA_1_list,self.volume_EMA_2_list,self.volume_EMA_3_list))
#        self.volume_EMA_1 = volume_EMA[0]
#        if self.time_num % 2 == 0:
#            self.volume_EMA_2 = volume_EMA[1]
#        if self.time_num % 3 == 0:
#            self.volume_EMA_3 = volume_EMA[2]
#        np.append(self.volume_EMA_1_list,self.volume_EMA_1)
#        np.append(self.volume_EMA_2_list,self.volume_EMA_2)
#        np.append(self.volume_EMA_3_list,self.volume_EMA_3)
#
#        RSI_EMA = self.calculate_variable_EMA(self.RSI,(self.RSI_EMA_1_list,self.RSI_EMA_2_list,self.RSI_EMA_3_list))
#        self.RSI_EMA_1 = RSI_EMA[0]
#        if self.time_num % 2 == 0:
#            self.RSI_EMA_2 = RSI_EMA[1]
#        if self.time_num % 3 == 0:
#            self.RSI_EMA_3 = RSI_EMA[2]
#        np.append(self.RSI_EMA_1_list,self.RSI_EMA_1)
#        np.append(self.RSI_EMA_2_list,self.RSI_EMA_2)
#        np.append(self.RSI_EMA_3_list,self.RSI_EMA_3)


    def calculate_derivative(self,list1,list2):
        try:
            derivative = (list1[-2] - list1[-1])/ (list2[-2] - list2[-1])
        except Exception,e:
            return 1

        return derivative

    def calculate_function(self):
        pass



    #    def derivative(self):
    #        self.EMA_1_derivative = self.calculate_derivative(self.EMA_1_list,self.time_num_list)
    #        np.append(self.EMA_1_derivative_list,self.EMA_1_derivative)
    #        self.EMA_2_derivative = self.calculate_derivative(self.EMA_2_list,self.time_num_list)
    #        self.EMA_3_derivative = self.calculate_derivative(self.EMA_3_list,self.time_num_list)
    #
    #        self.EMA_1_derivative_2 = self.calculate_derivative(self.EMA_1_derivative_list,self.time_num_list)
    #        np.append(self.EMA_1_derivative_2_list,self.EMA_1_derivative_2)

    def calculate_RSI(self):

        if len(self.s.price_list) > 2:

            gain_loss = self.s.price_list[-1] - self.s.price_list[-2]

            if gain_loss > 0:
                gain = gain_loss
                self.s.gain_list.append(gain)
            elif gain_loss < 0:
                loss = -gain_loss
                self.s.loss_list.append(loss)
            elif gain_loss == 0:
                self.s.gain_list.append(0)
                self.s.loss_list.append(0)

        current_gain_list = []
        current_loss_list = []

        if len(self.s.price_list) < 50:

            self.s.RSI = 50

        elif self.s.ptime % 5 == 0:

            for item in self.s.gain_list[-10:]:
                if not item == 0:
                    current_gain_list.append(item)

            for item in self.s.loss_list[-10:]:
                if not item == 0:
                    current_loss_list.append(item)

            try:
                gain = myavg(current_gain_list)
            except Exception, e:
                try:
                    gain = current_gain_list[-1]
                except Exception,e:
                    gain = 0
            try:
                loss = myavg(current_loss_list)

            except Exception, e:
                try:
                    loss = current_loss_list[-1]
                except Exception,e:
                    loss = 1

                    #                gain = (self.calculate_list_EMA(current_gain_list))
                    #                loss = (self.calculate_list_EMA(current_loss_list))

            RS = gain/loss

            self.s.RSI = (100 - (100/((1+RS))))

            self.s.RSI_list.append(self.RSI)

    def calculate_Integral(self,list):


        a = self.s.time_num_list[0]
        b = self.s.time_num_list[-1]
        n = len(list)/5

        dx = (b - a)/ n

        sum = 0

        for i,j,k,l,m in zip(list[0::1], list[1::2],list[2::3],list[3::4],list[4::5]):
            sum += k

        integral = dx * sum

        return integral



