'use client'

import { useState } from 'react'
import axios from 'axios'
import { Button } from "../ui/button"
import { Input } from "../ui/input"
import { Label } from "../ui/label"
import { Textarea } from "../ui/textarea"
import { Card, CardContent } from "../ui/card"
import { Plane, Loader2 } from 'lucide-react'
import { useToast } from "../ui/use-toast"
import TripPlanPage from './trip-plan-page'

interface FormData {
  age: string;
  gender: string;
  personality: string;
  days: string;
  origin: string;
  destination: string;
}

interface ItineraryDay {
  title: string;
  activities: {
    name: string;
    location: string;
    description: string;
    suitability: string;
    reviews: string;
  }[];
}

interface Itinerary {
  [key: string]: ItineraryDay;
}

export default function TravelForm() {
  const { toast } = useToast()
  const [formData, setFormData] = useState<FormData>({
    age: '',
    gender: '',
    personality: '',
    days: '',
    origin: '',
    destination: ''
  })
  const [isLoading, setIsLoading] = useState(false)
  const [itinerary, setItinerary] = useState<Itinerary | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      const response = await axios.post('http://localhost:5000/plan', formData)
      setItinerary(response.data.itinerary)
    } catch (error) {
      console.error('Error:', error)
      toast({
        title: "Error",
        description: "Failed to generate trip plan. Please try again.",
        variant: "destructive",
      })
    } finally {
      setIsLoading(false)
    }
  }

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target
    setFormData(prev => ({ ...prev, [name]: value }))
  }

  if (itinerary) {
    return <TripPlanPage itinerary={itinerary} destination={formData.destination} />
  }

  return (
    <div className="min-h-screen bg-[#E8C4B8] flex items-center justify-center">
      <div className="w-full max-w-4xl mx-auto p-4 md:p-8">
        <div className="text-center mb-8">
          <Plane className="mx-auto text-[#527A78] h-10 w-10 mb-6" />
          <h1 className="text-[#2D3648] text-4xl font-serif">Your Personal</h1>
          <h1 className="text-[#2D3648] text-4xl font-serif mb-2">Travel Planner</h1>
        </div>

        <Card className="bg-white/95 shadow-xl rounded-2xl">
          <CardContent className="p-12">
            <form onSubmit={handleSubmit} className="space-y-10">
              <div className="grid grid-cols-2 gap-8">
                <div className="space-y-3">
                  <Label htmlFor="age" className="text-gray-600 text-lg">Age</Label>
                  <Input
                    id="age"
                    name="age"
                    type="number"
                    required
                    value={formData.age}
                    onChange={handleInputChange}
                    className="border-gray-200 focus:border-[#527A78] focus:ring-[#527A78] bg-white h-12"
                  />
                </div>

                <div className="space-y-3">
                  <Label htmlFor="gender" className="text-gray-600 text-lg">Gender</Label>
                  <Input
                    id="gender"
                    name="gender"
                    type="text"
                    required
                    value={formData.gender}
                    onChange={handleInputChange}
                    className="border-gray-200 focus:border-[#527A78] focus:ring-[#527A78] bg-white h-12"
                  />
                </div>
              </div>

              <div className="space-y-3">
                <Label htmlFor="personality" className="text-gray-600 text-lg">Personality Traits</Label>
                <Textarea
                  id="personality"
                  name="personality"
                  required
                  value={formData.personality}
                  onChange={handleInputChange}
                  placeholder="e.g. adventurous, loves nature, enjoys local cuisine"
                  className="border-gray-200 focus:border-[#527A78] focus:ring-[#527A78] bg-white min-h-[160px] resize-none"
                />
              </div>

              <div className="grid grid-cols-3 gap-8">
                <div className="space-y-3">
                  <Label htmlFor="days" className="text-gray-600 text-lg">Number of Days</Label>
                  <Input
                    id="days"
                    name="days"
                    type="number"
                    min="1"
                    required
                    value={formData.days}
                    onChange={handleInputChange}
                    className="border-gray-200 focus:border-[#527A78] focus:ring-[#527A78] bg-white h-12"
                  />
                </div>

                <div className="space-y-3">
                  <Label htmlFor="origin" className="text-gray-600 text-lg">Origin</Label>
                  <Input
                    id="origin"
                    name="origin"
                    type="text"
                    required
                    value={formData.origin}
                    onChange={handleInputChange}
                    className="border-gray-200 focus:border-[#527A78] focus:ring-[#527A78] bg-white h-12"
                  />
                </div>

                <div className="space-y-3">
                  <Label htmlFor="destination" className="text-gray-600 text-lg">Destination</Label>
                  <Input
                    id="destination"
                    name="destination"
                    type="text"
                    required
                    value={formData.destination}
                    onChange={handleInputChange}
                    className="border-gray-200 focus:border-[#527A78] focus:ring-[#527A78] bg-white h-12"
                  />
                </div>
              </div>

              <Button
                type="submit"
                className="w-full bg-[#527A78] hover:bg-[#476866] text-white font-medium py-7 rounded-lg mt-6 text-lg"
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Planning your trip...
                  </>
                ) : (
                  <>✨ Plan My Perfect Trip</>
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {isLoading && <LoadingPage />}
      </div>
    </div>
  )
}

function LoadingPage() {
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-8 rounded-lg shadow-lg text-center">
        <Loader2 className="animate-spin h-12 w-12 text-[#527A78] mx-auto mb-4" />
        <p className="text-xl font-semibold text-gray-800">Planning your perfect trip...</p>
        <p className="text-gray-600 mt-2">This may take a few moments</p>
      </div>
    </div>
  )
}

